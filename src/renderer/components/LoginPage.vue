<template>
 <div>
    <div class="wrapper">
        <main>
            <div class="info-column columns is-gapless">
                <div class="left-column column">
                    <div class="show-box container">
                        <div class="tile">
                            <div class="tile is-vertical">
                                <div class="tile">
                                    <div class="show-header">
                                        <div class="software-logo"></div>
                                        <div class="software-name">
                                            <h1 class="title is-3 has-text-white">生物特征录入器</h1>
                                        </div>
                                    </div>
                                </div>
                                <div class="tile">
                                    <div class="software-brief has-text-white">
                                    <span>生物特征录入器完成指纹，人脸图像的采集工作，将数据采集后进行特征提取，将特征数据上传云端服务器保存
                                    </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="right-column column">
                    <div class="login-box container">
                        <div class="tite is-ancestor">
                            <div class="tite is-vertical login-form">
                                <div class="tite">
                                    <div class="field login-header">
                                        <div class="control">
                                            <h1 class="login-title title is-5">管理员登录</h1>
                                        </div>
                                    </div>
                                </div>
                                <div class="tile">
                                    <div class="field">
                                        <div class="control has-icons-left has-icons-right">
                                            <input id="username" v-model="username" class="input is-success" type="text" placeholder="请输入账号" >
                                            <span class="icon is-small is-left">
                                            <i class="fa fa-user"></i>
                                            </span>
                                            <span class="icon is-small is-right">
                                            <i class="fa"></i>
                                            </span>
                                        </div>
                                        <p class="help" v-bind:class="{ 'is-danger': username_promt }">{{username_promt}}</p>
                                    </div>
                                </div>
                                <div class="tile">
                                    <div class="field">
                                        <div class="control has-icons-left has-icons-right">
                                            <input id="password" v-model="password" class="input is-success" type="password" placeholder="请输入密码" >
                                            <span class="icon is-small is-left">
                                            <i class="fa fa-key"></i>
                                            </span>
                                            <span class="icon is-small is-right">
                                            <i class="fa"></i>
                                            </span>
                                        </div>
                                        <p class="help" v-bind:class="{ 'is-danger': password_promt }" >{{password_promt}}</p>
                                    </div>
                                </div>
                                <div class="tile">
                                    <div class="field remeber-me">
                                        <div class="control">
                                            <label class="checkbox">
                                            <input id="remeber-me" v-model="is_remeber" type="checkbox">
                                            记住密码
                                            </label>
                                        </div>
                                    </div>
                                </div>
                                <div class="tile">
                                    <div class="field">
                                        <div class="control">
                                            <button id="submit" v-on:click="login" class="button is-primary is-fullwidth">登录</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
        <div class="login-footer">
            <div class="items columns ">
                <span class="item column">
                    <a href="#" class="has-text-grey">管理中心</a>
                </span>
                <span class="item column">
                    <a href="#" class="has-text-grey">使用教程</a>
                </span>
                <span class="item column">
                    <a href="#" class="has-text-grey">账号申请</a>
                </span>
                <span class="item column">
                    <a href="#" class="has-text-grey">关于</a>
                </span>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import constant from '../constant/constant.vue'



export default {
    name: 'login-page',
    data() {
        return {
            username: '',
            password: '',
            is_remeber: false,
            username_promt: '',
            password_promt: ''
        }
    },
    created() {

    },
    methods: {
        validate(){
            this.username_promt = ''        
            this.password_promt = ''

            if (this.username == '') {
                this.username_promt = constant.login.USERNAME_PROMT
            }
            if (this.password == '') {
                this.password_promt = constant.login.PASSWORD_PROMT
            }

            if (this.username == '' || this.password == ''){
                return false
            }
            
            return true
        },
        login(){
            if(this.validate()) {
                // todo 发送请求



                // 是否记住登录状态
                if (this.is_remember) {
                    // 存储token
                }
            }
        },
        success() {

        },
        failure(err){
            
        }
    }
}
</script>

<style>

  .wrapper {
    position: relative;
    height: 100vh;
    padding: 60px 80px;
    width: 100vw;
    background: hsl(0, 0%, 96%);
  }
  main {
    position: absolute;
    top: 50%;left: 50%;
    transform: translate(-50%, -50%);
    height: 500px;
    width: 800px;
    background: hsl(171, 100%, 41%);
    box-shadow:7px 5px 25px #7A7A7A;
    border-radius: 15px;
  }
  .left-column {
      position: relative;
  }
  .show-box {
      position: relative;
      top: 25%;left: 0;
      height: 300px;
      width: 300px !important;
  }
  .left-column .show-box .software-brief {
      position: relative;
      left: 0;top: 50px;

  }
  .info-column {
      height: 100%;
  }
  .right-column {
      background: white;
      border-radius: 0 15px 15px 0;
  }
  .login-box {
    position: absolute;
    top: 50%;left: 50%;
    transform: translate(-50%, -50%);
  }
  .right-column .login-form {
      width: 260px;
      margin: 0 auto;
  }
  .right-column .login-form .login-header, .remeber-me {
      margin-bottom: 20px;
  }
  .right-column .login-form .help{
      height: 20px;
  }
  .right-column .login-form .login-title{
      text-align: center;
  }
  .right-column .login-form #submit{
      width: 258px;
  }
  .left-column{
    height: 100%;
  }

  .login-footer {
      position: absolute;
      bottom: 7%;left: 0;  right: 0; 
      text-align: center; 
  }
  .login-footer .items {
      width: 400px;
      margin: 0 auto;
  }
  

</style>