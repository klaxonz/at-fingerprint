<template>
  <div class="wrapper">
      <div class="container">
        <div class="columns">
          <div class="column is-4 ">
            <div class="left-side">
              <div class="box ">
                <div class="finger-image-box">
                  <figure class="image">
                    <img :src="imgFilename" alt="">
                  </figure>
                </div>
              </div>
              <div class="box">
                <div class="open-device-box">
                  <div class="level">
                    <div class="level-item">
                      <button  v-on:click="openSerial" class="button is-primary" v-if="portSelected == '无'" disabled>打开</button>
                      <button  v-on:click="openSerial" class="button is-primary" v-else>打开</button>
                    </div>
                    <div class="level-item">
                      <button v-on:click="getEnableSerial" class="button is-primary">搜索</button>
                    </div>
                    <div class="level-item">
                      <div class="field">
                        <div class="control">
                          <div class="select is-primary">
                            <select v-model="portSelected">
                              <option v-for="port in portsList" :value="port.path" :key="port.path">{{port.path}}</option>
                            </select>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="box">
                <div class="select-device-config-box">
                  <div class="level">
                    <div class="level-item"><h1 class="title is-7">波特率设置</h1 ></div>
                    <div class="level-item"><h1 class="title is-7" >数据包大小/字节</h1></div>
                    <div class="level-item"><h1 class="title is-7">安全等级</h1></div>
                  </div>
                  <div class="level">
                    <div class="level-item">
                      <div class="field">
                        <div class="control">
                          <div class="select is-small is-primary">
                            <select v-model="baudSelected">
                              <option v-for="baudrate in baudrateList" :value="baudrate.rate" :key="baudrate.key">{{baudrate.rate}}</option>
                            </select>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="level-item">
                      <div class="field">
                        <div class="control">
                          <div class="select is-small is-primary " >
                            <select v-model="packetSizeSelected">
                              <option v-for="packetSize in packetSizeList" :value="packetSize.size" :key="packetSize.key">{{packetSize.size}}</option>
                            </select>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="level-item">
                      <div class="field">
                        <div class="control">
                          <div id="baudrate" class="select is-small is-primary">
                            <select v-model="secureSelected">
                              <option v-for="secure in secureLevel" :value="secure.level" :key="secure.key">{{secure.level}}</option>
                            </select>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
          </div>
          <div class="column">
            <div class="right-side">
              <div class="box">
                <div class="show-info-box">
                  <p class="message is-size-5 has-text-weight-bold has-text-danger">{{message}}</p>
                </div>
              </div>
              <div class="box">
                <div class="handle-data-box">
                  <div class="level">
                    <div class="level-item">
                      <h1 class="title is-6">查询学生</h1>
                    </div>
                    <div class="level-item">
                      <input class="input is-rounded" type="text" placeholder="姓名/编号/身份证">
                    </div>
                    <div class="level-item">
                      <div class="handle-button">
                        <button class="button is-primary">查询</button>
                        <button class="button ">上传</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="box">
                <div class="image-manage">
                  <div class="level">
                    <div class="level-left">
                      <div class="level-item">
                        <button class="button" v-on:click="addFinger">指纹录入</button>
                      </div>
                      <div class="level-item">
                        <button class="button">获取图像</button>
                      </div>
                      <div class="level-item">
                        <button class="button">下载图像</button>
                      </div>
                    </div>
                    <div class="level-right">
                      <div class="level-item">
                        <label class="checkbox">
                          <input type="checkbox">显示图像
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="box">
                <div class="finger-manage">
                  <div class="level">
                    <div class="level-left">
                      <div class="level-item">
                        <button class="button">取消操作</button>
                      </div>
                      <div class="level-item">
                        <button class="button">关闭设备</button>
                      </div>
                      <div class="level-item">
                        <button class="button">关闭设备</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
  </div>
</template>

<script>
import { PythonShell } from 'python-shell'
import serial from "../util/serial"
import path from 'path'

export default {
    name: 'fingerprint-page',
    data() {
        return {
          portsList: [],
          portSelected: '',
          baudrateList: [],
          baudSelected: '',
          packetSizeList: [],
          packetSizeSelected: '',
          secureLevel: [],
          secureSelected: '',
          message: '',
          imgFilename: '../../../image/' + 'finger_1586376786.bmp'
        }
    },
    created() {
      this.init()
    },
    methods: {
      init(){
        this.getEnableSerial()
        this.initDeviceParam()

        if (this.portsList.length == 0 || this.portSelected == '无'){
          this.message = '点击 [搜索] 按钮，查询可用设备'
        } else {

        }


      },
      openSerial(){
        // 打开选择的串口设备
        let _this = this
        serial.openSerial(this.portSelected, function(result){
          if (Object.keys(result).length > 0 && result.code == 0) {
             let data = result.data
             _this.baudSelected       = data.baudrate
             _this.packetSizeSelected = data.packetSize
             _this.secureSelected     = data.secureLevel

             _this.message = "设备连接成功"
          } else {
             _this.message = "连接设备失败，请检查设备是否连接！"
          }
        })
      },
      getEnableSerial(){
        
        serial.listSerial().then((ports) => {

          this.portsList.forEach(port => {
            this.portsList.pop()
          })

          ports.forEach(port => {
            this.portsList.push(port)
          });
        }).then(()=>{
          if (this.portsList.length == 0) {
    
            let defaultPort  = {
              "path": "无",
              "manufacturer": "",
              "serialNumber": "",
              "pnpId": "",
              "locationId": "",
              "vendorId": "",
              "productId": ""
            }
            this.portsList.push(defaultPort)
            this.message = '无设备已连接，请检查是否正常连接'
            this.portSelected = this.portsList[0].path

          } else {
            this.message = '请选择设备，点击 [打开] 按钮连接设备'
            this.portSelected = this.portsList[0].path
          }

        })
      },
      initDeviceParam(){
        // 波特率初始化
        let baudseed = 9600
        for(let i = 1; i < 13; i++){
          this.baudrateList.push({
            key: '' + baudseed * i,
            rate: '' + baudseed * i
          })
        }
        this.baudSelected = this.baudrateList[5].rate

        // 数据包大小初始化
        let packetSizeSeed = 32
        for(; packetSizeSeed <= 256; packetSizeSeed <<= 1){
          this.packetSizeList.push({
            key: '' + packetSizeSeed,
            size: '' + packetSizeSeed
          })
        }
        this.packetSizeSelected = this.packetSizeList[3].size

        // 安全等级
        for (let i = 1; i < 6; i++) {
          this.secureLevel.push({
            key: '' + i,
            level: '' + i
          })
        }
        this.secureSelected = this.secureLevel[2].level

      },
      addFinger() {
        let scriptPath = path.join(process.cwd(), '/src/renderer/script/index.py')
        let options = {
            mode: 'text',
            pythonOptions: ['-u'],
            args: ['add']
        };

        let pyshell = new PythonShell(scriptPath, options);

        let data = {
            port: this.portSelected,
            baudrate: 57600,
        }

        let json_str = encodeURI(JSON.stringify(data), "utf-8")
        pyshell.send(json_str).end(function (err) {
            console.log(err)
        });

        let _this = this

        pyshell.on('message', function (message) {
            console.log(message)
            // 转化json数据
            data = JSON.parse(message)
            // 回调函数处理
            _this.message = data.message

            if (data.code == 0 && data.msg_code == 1000) {
              let filename = data.data.filename
              if (filename) {
                _this.imgFilename = '../../../' + filename
              }
            }

        })

        pyshell.on('stderr', function (stderr) {
            console.log(stderr)
        }).on('close', function () {

        }).end(function() {

        });

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
    /* background: hsl(0, 0%, 86%); */
      background-color: hsl(171, 100%, 41%);

  }
  .container {
      height: 100%;
      border: 3px solid white;
      background-color: hsl(171, 100%, 41%);
  }
  .box {
    box-shadow:7px 5px 25px #7A7A7A !important;
  }
  .columns {
    margin: 0 !important;
  }
  .column {
    height: 100%;
    /* background: hsl(171, 100%, 41%); */
  }

  .select-device-config-box .level:first-child{
    position: relative;
    top: 0;
    left: 5px;
    margin-bottom: 5px;
  }
  .show-info-box .message {
    height: 160px;
  }

  img {
      height: 256px !important;
      width: 256px !important;
      margin: 0 auto;
  }

</style>