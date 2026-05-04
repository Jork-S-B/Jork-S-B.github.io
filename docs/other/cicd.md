持续集成 (CI)

* 目标：快速发现集成错误，保障代码库质量
* 关键活动包括：1.代码扫描 2.单元测试 3.集成或接口测试 4.构建

持续交付/部署 (CD)

* 目标：将通过验证的制品，安全、高效地交付到生产环境
* 关键活动包括：1.自动化部署到测试、预生产环境 2.端到端测试（在拟真环境验证完整流程） 3.性能/合规测试 4.生产发布

## 📌 阶段一：CI分支代码验证

触发方式：手动构建、代码提交时触发、tag提交时触发、定时任务、级联其他流水线触发等

分支push -> 进行通知 -> SonarQube/EOS扫描 -> Maven构建 -> Junit单元测试 -> 代码构建（jar、war等） -> 打包临时镜像容器化部署到测试环境 
-> 自动化测试（验证该分支与其他系统协作、单分支在目前场景下是否有异常等）

## 📌 阶段二：CI主干代码合并流程

触发方式：分支测试完成后合代码

合并生成临时tag，合并异常时人工介入 -> master代码，SonarQube/EOS扫描 ->  Maven构建 -> Junit单元测试 -> 代码构建 -> 打包临时镜像容器化部署到测试环境 
-> 自动化测试

## 📌 阶段三：CD Release发布

选择主干临时tag -> 生成Release分支打版本tag -> Release代码 -> docker镜像构建 -> Trivy安全检查 -> 
镜像上传至harbor（镜像库），更新helm chart（专门管理发布脚本），其他相关资源上传（如sql脚本，手工执行且有回滚预案） -> 发版完成通知

## 📌 阶段四：部署应用

Helm执行脚本，驱动k8s从harbor拉取指定镜像、运行pod -> 自动化/人工验证 -> 部署完毕通知 -> 发布（应用对外可见） 


## 📌 Q&A

Q1: 平时在 CI/CD 方面有没有接触？

先举个人实验，再举工作例子。

A: 通过 GitHub Actions 搭建过一个文档站点的自动部署流水线（.github/workflows/gh-deploy.yml，工作流编排） – 代码 push 到 main 分支后，自动拉代码、安装 Python 依赖（mkdocs 等）、然后通过 mkdocs build 构建、mkdocs gh-deploy 发布到 GitHub Pages。

在测试工作中把同样思路迁移到了测试流水线里：用 Jenkins pipeline 实现 PR 自动触发接口测试（pytest --alluredir=results；actions/upload-artifact 上传测试报告等）；添加质量门禁（成功率、覆盖率）；测试结果通过 Allure 报告归档，并自动通知。