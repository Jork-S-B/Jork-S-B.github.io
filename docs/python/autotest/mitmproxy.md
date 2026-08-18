通过mitmproxy库能实现类似Fiddler抓包工具的功能，也适用于APP，但处理HTTPS请求前需要安装及配置证书。

参考资料：[mitmproxy的使用以及遇到的问题](https://blog.csdn.net/feiyu68/article/details/119665869)

代码示例可参考：[使用mitmproxy+jinja2，捕获请求并生成对应的接口测试用例](https://gitee.com/Jork-S-B/basic-auto-test/blob/master/Commons/my_proxy/api_proxy.py)

---

基于mitmproxy开发的mock服务，解决第三方强依赖的痛点。

简单示例：支付请求提交成功，返回成功响应，并通过多线程异步返回回调报文（如订单的子订单号等）。

## 目录结构

```text
main.py
├── config/               # 配置管理
├── projects/             # 业务项目模块，按业务领域划分
│   ├── project1/
│   └── project2/
├── utils/                # 工具库：配置加载、日志、加解密等
└── varify_mock/          # Mock服务验证脚本
    ├── app.py
    ├── mock_engine.py
    └── mock_script.py
```

### 动态路由&热插拔

实现步骤: 

1. 动态模块发现(main.py:16-41)

    - 使用 pkgutil.iter_modules() 扫描 projects/ 目录
    - 通过 importlib.import_module() 动态加载模块
    - 检测模块是否实现了 handle_request(flow, api_path) 函数

2. 动态路由分发(main.py:49-106): 根据请求路径格式分发，如：/projects/{project_name}/{api_path}
3. 热插拔，重启服务后自动加载新项目。需要创建 handler 文件，且必须实现 handle_request 函数

=== "projects\wuhaomin\whm.py"

    ```python
    import re
    from datetime import datetime

    from mitmproxy import http
    import json
    import datetime

    from utils.encryption_decryption import encrypt_aes
    from utils.log_utils import logger


    def handle_request(flow: http.HTTPFlow, api_path: str) -> bool:
        """whm测试Mock请求"""
        api_path = api_path.split('?')[0]
        # 新增：测试接口 - 处理 /test/{id}/v1/mf
        test_aes_match = re.match(r"/test/(\d+)/v1/mf$", api_path)

        if flow.request.method == "GET" and test_aes_match:
            # 处理测试接口
            test_id = test_aes_match.group(1)
            logger.info(f"测试AES加密接口，参数ID: {test_id}")
            _test_aes_encryption(flow, test_id)
            return True
        return False

    def _test_aes_encryption(flow: http.HTTPFlow, test_id: str):
        """
        测试AES加密接口
        访问: GET http://localhost:30080/projects/wuhaomin/test/123/v1/mf
        返回: AES加密后的123
        """
        try:
            logger.info(f"开始AES加密处理，参数: {test_id}")
            KEY_SEED = "i9DO9V2i9Yu2436w3456409L91A28wbA"
            # 使用工具类中的AES加密函数
            encrypted_data = encrypt_aes(test_id, KEY_SEED)
            
            if encrypted_data:
                # 构造响应数据
                response_data = {
                    "original": test_id,
                    "encrypted": encrypted_data,
                    "message": "AES加密成功",
                    "timestamp": datetime.datetime.now().isoformat()
                }
                
                logger.info(f"AES加密完成，原始数据: {test_id}, 加密结果: {encrypted_data}")
                
                flow.response = http.Response.make(
                    200,
                    json.dumps(response_data, ensure_ascii=False).encode('utf-8'),
                    {"Content-Type": "application/json;charset=UTF-8"}
                )
            else:
                # 加密失败
                error_msg = {"error": "AES加密失败"}
                logger.error("AES加密失败")
                flow.response = http.Response.make(
                    500, 
                    json.dumps(error_msg).encode('utf-8'), 
                    {"Content-Type": "application/json"}
                )
                
        except Exception as e:
            error_msg = {"error": f"服务器内部错误: {str(e)}"}
            logger.error(f"测试AES加密接口错误: {e}", exc_info=True)
            flow.response = http.Response.make(
                500, 
                json.dumps(error_msg).encode('utf-8'), 
                {"Content-Type": "application/json"}
            )
    ```

### Jenkinsfile & k8s_deployment

=== "Jenkinsfile"

    ```pipeline
    // 动态生成版本号
    def createVersion() {
        return new Date().format('yyyyMMdd') + "_${env.BUILD_ID}"
    }

    pipeline {
        agent any

        parameters {
            choice(name: 'BRANCH', choices: ['master'], description: '要构建的Git分支名称')
            choice(name: 'ENV', choices: ['test'], description: '部署环境')
            string(name: 'REPLICAS', defaultValue: '2', description: 'K8s副本数量')
        }

        environment {
            // ---【核心配置】---
            BUILD_VERSION = createVersion()

            // 项目配置
            GIT_URL = 'https://xx.git'
            IMAGE_NAME = 'mitmproxy-mock-service' // 镜像名称
            K8S_DEPLOYMENT_NAME = 'mock-service-deployment' // K8s Deployment 的实际名称
            FULL_WORK_DIR = "./"
            DOCKERFILE_PATH = "Dockerfile" // Dockerfile 相对仓库根目录的路径
            DEPLOY_CONFIG_PATH = "k8s_deployment.yaml" // K8s 模板文件路径

            // 镜像仓库配置
            // IMAGE_REGISTRY = 'xx.images.com' // 部署时使用的仓库
            IMAGE_NAMESPACE = "${params.ENV}" // 命名空间使用环境名

            // K8s 资源限制
            CPU_LIMITS = "2"
            MEMORY_LIMITS = "4Gi"
            REPLICAS = "${params.REPLICAS}"

            // 凭据 ID
            GIT_CREDS_ID = 'git-account-jenkins' // jenkins的git凭证
            K8S_CONNECT_FILE = 'kubeconfig-test'

        }

        stages {
            stage('代码拉取') {
                steps {
                    git branch: params.BRANCH,
                        credentialsId: env.GIT_CREDS_ID,
                        url: env.GIT_URL
                    sh "git log -1 --oneline"
                }
            }

            stage('镜像构建与推送') {
                steps {
                    script {
                        def fullImageName = "${env.IMAGE_REGISTRY}/${env.IMAGE_NAMESPACE}/${env.IMAGE_NAME}:${env.BUILD_VERSION}"
                        def latestImageName = "${env.IMAGE_REGISTRY}/${env.IMAGE_NAMESPACE}/${env.IMAGE_NAME}:latest"

                        echo "Preparing to build and push image: ${fullImageName}"

                        // 步骤 1: 使用 withCredentials 安全地获取凭据并登录
                        // 我们不再使用 docker.withRegistry，而是手动登录
                        withCredentials([usernamePassword(credentialsId: env.REGISTRY_CREDS_ID, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                            // 使用 --password-stdin 是一种更安全的登录方式，避免密码出现在进程列表中
                            sh "echo \$DOCKER_PASS | docker login ${env.IMAGE_REGISTRY} -u \$DOCKER_USER --password-stdin"
                        }

                        // 步骤 2: 执行构建、推送和清理
                        try {
                            // 构建镜像
                            echo "Building Docker image from context '.'..."
                            sh "docker build -t ${fullImageName} -f ${env.DOCKERFILE_PATH} ."

                            // 为镜像打上 latest 标签
                            sh "docker tag ${fullImageName} ${latestImageName}"

                            // 推送带版本号的镜像
                            echo "Pushing versioned image: ${fullImageName}"
                            sh "docker push ${fullImageName}"

                            // 推送 latest 标签的镜像
                            echo "Pushing latest image: ${latestImageName}"
                            sh "docker push ${latestImageName}"

                        } finally {
                            // 步骤 3: 无论成功与否，都尝试登出并清理本地镜像，保持 Agent 干净
                            echo "Cleaning up local images and logging out..."
                            sh "docker rmi ${fullImageName} || true"
                            sh "docker rmi ${latestImageName} || true"
                            sh "docker logout ${env.IMAGE_REGISTRY}"
                        }
                    }
                }
            }

            stage('K8s部署') {
                steps {
                    script {
                        withCredentials([file(credentialsId: env.K8S_CONNECT_FILE, variable: 'KUBECONFIG')]) {
                            def fullImageName = "${env.IMAGE_REGISTRY}/${env.IMAGE_NAMESPACE}/${env.IMAGE_NAME}:${env.BUILD_VERSION}"

                            echo "Deploying to Kubernetes..."
                            echo "  Namespace: ${params.ENV}"
                            echo "  Service Name: ${env.K8S_DEPLOYMENT_NAME}"
                            echo "  Image: ${fullImageName}"

                            // 使用 sed 动态替换模板中的变量
                            sh """
                                sed -e "s#\\\${NAMESPACE}#${params.ENV}#g" \
                                -e "s#\\\${SERVICE_NAME}#${env.K8S_DEPLOYMENT_NAME}#g" \
                                -e "s#\\\${IMAGE}#${fullImageName}#g" \
                                -e "s#\\\${CPU_LIMITS}#${env.CPU_LIMITS}#g" \
                                -e "s#\\\${MEMORY_LIMITS}#${env.MEMORY_LIMITS}#g" \
                                -e "s#\\\${REPLICAS}#${env.REPLICAS}#g" \
                                ${env.DEPLOY_CONFIG_PATH} > processed.yaml

                                echo "===== Generated K8s Config ====="
                                cat processed.yaml
                                echo "=============================="

                                kubectl apply -f processed.yaml --kubeconfig="$KUBECONFIG"
                            """

                            // 验证部署状态
                            sh """
                                kubectl rollout status deployment/${env.K8S_DEPLOYMENT_NAME} \
                                    -n ${params.ENV} \
                                    --timeout=300s \
                                    --kubeconfig="$KUBECONFIG"
                            """
                        }
                    }
                }
            }
        }

        post {
            always {
                echo "Pipeline finished for version ${env.BUILD_VERSION}."
            }
        }
    }
    ```

=== "k8s_deployment.yaml"

    ```yaml
    # Deployment 资源
    apiVersion: apps/v1
    kind: Deployment
    metadata:
    name: ${SERVICE_NAME}
    namespace: ${NAMESPACE}
    labels:
        app: ${SERVICE_NAME}
    spec:
    replicas: ${REPLICAS}
    selector:
        matchLabels:
        app: ${SERVICE_NAME}
    template:
        metadata:
        labels:
            app: ${SERVICE_NAME}
        spec:
        imagePullSecrets:  # 测试环境镜像拉取凭据
            - name: paas.image.registry.test
        containers:
            - name: ${SERVICE_NAME} # 容器名称使用SERVICE_NAME
            image: ${IMAGE}
            imagePullPolicy: Always # 推荐使用Always来确保拉取最新镜像
            ports:
                - containerPort: 8080 # mitmproxy监听的端口
                name: http
                protocol: TCP
            resources:
                requests: # 为 Python 服务设置合理的资源请求
                cpu: "2"
                memory: "2Gi"
                limits:
                cpu: "${CPU_LIMITS}"
                memory: "${MEMORY_LIMITS}"
    #          livenessProbe:
    #            tcpSocket:
    #              port: 8080
    #            initialDelaySeconds: 15
    #            periodSeconds: 20
    #          readinessProbe:
    #            tcpSocket:
    #              port: 8080
    #            initialDelaySeconds: 5
    #            periodSeconds: 10
    ---
    # Service 资源
    apiVersion: v1
    kind: Service
    metadata:
    name: ${SERVICE_NAME}
    namespace: ${NAMESPACE}
    spec:
    selector:
        app: ${SERVICE_NAME}
    ports:
        - name: http
        port: 80 # Service 对外暴露 80 端口
        protocol: TCP
        targetPort: 8080 # 将流量转发到容器的 80 端口
    ```

## 正向代理&反向代理

- 正向代理: 用户通过代理服务器，突破访问限制，如科学上网、内网员工（通过代理服务器）访问限制外的网站。
- 反向代理: 客户端不知道自己在访问具体的哪台后台服务器，只看到反向代理服务器。经典的反向代理工具有[nginx](/other/nginx_notes/)、haproxy等。

该mock服务，以及mitmproxy默认启用的模式都属于正向代理: 客户端能感知到，且需手动设置代理。