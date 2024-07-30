- mvvm，model-view-viewmodel。
- 渐进式，只需用部分规则。
- 双向数据绑定，vue.js会自动响应数据变化，对数据和视图进行修改。
- 组件化，将父组件拆分多个子组件，子组件封装成类似于类的形式，传入方法和参数的定义即可，但尽量不要在子组件修改父组件的属性。

依赖环境: node14、npm6

|                           命令                           | 说明          |
|:------------------------------------------------------:|:------------|
| npm config set registry https://registry.npmmirror.com | 更换镜像源       |
|              npm install --global vue-cli              | 全局安装vue-cli |
|                 vue init webpack demo                  | 创建项目        |
|                      npm install                       | 导入项目需安装依赖   |
|                      npm run dev                       | 启动          |
|                     npm run build                      | 构建          |

## 📌 使用模版

一般包括模板-template、样式-style、脚本-script

### 🚁 生命周期

|     钩子函数      | 说明                            |
|:-------------:|:------------------------------|
| beforeCreate  | 创建前，data和methods中的数据初始化前      |
| ***created*** | 创建后，data和methods中的数据初始化后      |
|  beforeMount  | 载入前，模板已经在内存中编译完成，但是尚未挂载到页面中。  |
| ***mounted*** | 载入后，挂载到页面，dom节点加载完成。          |
| beforeUpdate  | 更新前，内存的数据加载/同步到页面前。           |
|    Updated    | 更新后，内存的数据加载/同步到页面前后。          |
| beforeDestroy | 销毁前                           |
|   destroyed   | 销毁后                           |
|   activated   | 组件激活时，组件实例被激活时使用，用于重复激活一个实例时。 |
|  deactivated  | 组件未激活时                        |
| errorCaptured | 错误调用，当捕获一个来自后代组件的错误时调用。       |

### 🚁 脚本语法

|     语法     | 说明               |
|:----------:|:-----------------|
|    name    | 声明组件名称           |
|    data    | 声明变量/数据          |
| components | 注册/加载组件          |
|   props    | 定义组件的入参，该入参可以是函数 |
|  methods   | 声明js函数           |
|   watch    | 监听参数             |
|  computed  | 对参数进行简单计算，结果可存缓存 |

```vue

<script>
  // 引用其他模版定义的组件，搭配components使用
  import example from "@/views/example"  // @代表src路径
  // 导入组件
  export default {
    name: 'demo',
    data() {
      return {
        text: 'hello world',
        html: '<h1>hello world</h1>',
        list: [],
        isShow: true,
        form: {},
        arr: null,
        date: 20002222222, // 时间戳
      }
    },
    // 注册组件
    components: {
      example
    },
    // 定义组件的入参，类似python的init(id: str)
    props: {
      id: {
        type: String,
        default: '1'
      },
      // getUser: Function,
    },
    // 声明js函数
    methods: {
      submit(id, name) {
        /* 
          const a = 1; // 声明常量
          let b = 2; // 声明局部变量，仅当前代码块有效
          var c = 3; // 声明局部变量
         */
        this.$post('/api/xxx', this.form, res => {
          console.log(res)
        })
      }
    },
    watch: {
      id(newVal) {
        console.log(newVal)
      }
    },
    computed: {
      dateStr() { // 时间戳转为日期格式
        return this.date.format('yyyy-MM-dd')
      }
    },
    // 钩子函数
    created() {
    },
    beforeCreate() {
      // this.$store.commit('set_token', localStorage.getItem('token'));
      // this.$store.commit('set_user', JSON.parse(localStorage.getItem('user')));
    }
  }
</script>
```

### 🚁 模版语法

#### 🔧 插值

- {{text}}: 插入文本
- v-html: 插入文本，以html语法进行渲染，动态生成页面，如测试报告
- v-bind: 单向绑定，`v-bind`可省略为`:`符号
- v-model: 双向绑定，表单数据跟js里的数据会同步。

```vue

<template>
  <div>
    <a href="#">{{text}}</a>
    <span v-html="text"></span>
    <!-- 这里的v-bind:value可省略为:value -->
    <input class="user-account" type="text" v-bind:value="text"/>
  </div>
</template>
```

#### 🔧 事件绑定

v-on: 绑定事件，可省略为`@`符号。

`this.$emit`，用于从子组件向父组件发送自定义事件。

=== "@/views/mylogin.vue"

    ```vue
    <template>
      <div>
        <input type="text" v-model="account1"/>
        <input type="password" v-model="password1"/>
        <button v-on:click="submit">提交</button>
      </div>
    </template>
    <script>
    export default {
      name: 'login',
      props: {
        account: String,
        password: String
      },
      data() {
        return {
          account1: this.account,
          password1: this.password
        }
      },
      methods: {
        submit() {
          // this.$emit，用于子组件向父组件发送自定义事件，这里是把账号和密码传回父组件打印在console
          // 在子组件不能修改父组件的属性值
          this.$emit("submit", {account: this.account1, password: this.password1})
        }
      }
    }
    </script>
    ```

=== "@/views/demo.vue"

    ```vue
    <template>
      <div>
        <!-- @submit="submit($event)"，绑定子组件的事件 -->
        <login :account="form.account" :password="form.password" @submit="submit($event)"/>
      </div>
    </template>
    <script>
    import login from './mylogin'
    export default {
      name: 'demo',
      data() {
        return {
          form: {
            account: "123",
            password: "123"
          },
        }
      },
      components: {
        login
      },
      methods: {
        submit(form) {
          console.log(form)
        }
      },
    }
    </script>
    ```

#### 🔧 条件加载

- v-if: true时加载，false时销毁dom元素。另外相对的还有`v-else-if`、`v-else`。
- v-show: true时显示，false时隐藏。通过修改css样式`style="display: none;"`隐藏。

```vue

<template>
  <div>
    <input v-if="isShow" type="text" v-model="account1"/>
    <input v-else type="text" v-model="account2"/>
    <input v-show="isShow" type="text" v-model="account1"/>
    <button @click="submit">点击</button>
  </div>
</template>
<script>
  export default {
    name: 'demo',
    data() {
      return {
        account1: "123",
        account2: "这里是else",
        isShow: true,
      }
    },
    methods: {
      submit() {
        this.isShow = !this.isShow;
      }
    }
  }
</script>
```

#### 🔧 循环加载

```vue

<template>
  <div>
    <ul>
      <li v-for="item in loopList" :key="item">{{item}}</li>
      <br/>
      <li v-for="item in loopList2" :key="item">{{item.a}}</li>
    </ul>
  </div>
</template>
<script>
  export default {
    name: 'demo',
    data() {
      return {
        loopList: ['xxxx', 1, 2, 3, 4],
        loopList2: [{"a": 1}, {"a": 1}, {"a": 1}],
      }
    },
  }
</script>
```

#### 🔧 样式绑定

- `:style="{属性名: var}"`
- `:style="[{属性名: var}]"`
- `:class="var"`: 将css名作为参数传入
- `:class="{var: true}"`: 将css以对象的形式传入
- `:class="[{var: true}, {css1: flag}]"`: 传入多个css对象的数组

```vue

<template>
  <div>
    <input :class="cla" v-if="isShow" type="text" v-model="account1"/>
    <input :style="{width: mywidth}" v-show="isShow" type="text" v-model="account1"/>
    <button @click="changecss">点击</button>
  </div>
</template>
<script>
  export default {
    name: 'login',
    data() {
      return {
        account1: "123",
        isShow: true,
        mywidth: "100px",
        cla: "input1"
      }
    },
    methods: {
      changecss() {
        if (this.cla === "input1") {
          this.cla = "input2"
        } else {
          this.cla = "input1"
        }
      }
    }
  }
</script>
<style>
  .input1 {
    width: 200px;
    color: red
  }

  .input2 {
    width: 50px;
  }
</style>
```

## 📌 状态管理

vuex是一个专为vue应用程序开发的状态管理库，使组件间共享变量更容易。

安装vuex: npm install vuex@3 --save

### 🚁 vuex属性

- state: 存储数据，调用方式如`this.$store.state.var`
- mutations: 唯一可直接修改state数据的地方；通过commit调用，`this.$store.commit('mutations_func',val)`
- actions: 异步操作，实际上内部方法也是调mutations；通过dispatch调用，`this.$store.dispatch('action_func',val)`
- getters: 与computed类似，获取state数据进行简单计算，结果可存缓存，且原state的数据不变；通过getters调用，`this.$store.getters.var`
- modules: 模块化管理，每个模块拥有自己的state、mutation、action、getter。另外当namespaced属性值为true，使用时须加上模块名如`this.$store.state.module_name.var`

#### 🔧 局限性

vuex数据在刷新或者新窗口时会丢失/重置。

解决方案：使用`localstorage`或`sessionstorage`保存

=== "@/vuex/store.js"

    ```vue
    import Vue from 'vue';
    import Vuex from 'vuex';
    
    Vue.use(Vuex);
    // 登录验证
    export default new Vuex.Store({
        state: {
            user: null,
        },
        mutations: {
            // 登录
            set_user(state, user) {
                state.user = user;
            },
            // 注销
            del_user(state) {
                state.user = null;
                localStorage.removeItem("user");
            },
        },
    })
    ```

=== "@/views/mylogin.vue"

    ```vue
    <template>
      <div>
        <input type="text" v-model="account1"/>
        <button @click="submit">提交</button>
        <button @click="login">登录</button>
      </div>
    </template>
    <script>
    export default {
      name: 'login',
      data() {
        return {
          account1: "123",
        }
      },
      methods: {
        submit() {
          console.log(this.$store.state.user) // 首次提交用户为空
        },
        login(){
          console.log("模拟用户登录，并存入localStorage")
          this.$store.commit("set_user", "用户1")
          localStorage.setItem("user", "用户1") // 相对的也有getItem("var_name")
        }
      }
    }
    </script>
        ```