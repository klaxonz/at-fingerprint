import { PythonShell } from 'python-shell'
import SerialPort from 'serialport'
import path from 'path'


const serial = {
    scriptPath:path.join(process.cwd(), '/src/renderer/script/index.py'),
    openSerial: function(port, callback) {
        let options = {
            mode: 'text',
            pythonOptions: ['-u'],
            args: ['gparams']
        };
    
        let pyshell = new PythonShell(this.scriptPath, options);
        
        let data = {
            port: port,
            baudrate: 57600,
        }
        
        let json_str = encodeURI(JSON.stringify(data), "utf-8")
        pyshell.send(json_str).end(function (err) {
            console.log(err)
        });

        pyshell.on('message', function (message) {
            console.log(message)
            // 转化json数据
            data = JSON.parse(message)
            // 回调函数处理
            callback(data)
        })

        pyshell.on('stderr', function (stderr) {
            console.log(stderr)
        }).on('close', function () {
        }).end(function() {
        });
     

      
      
    },
    listSerial: function() {
        return SerialPort.list()      
    },

}

export default serial

