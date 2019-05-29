var express = require('express')
const Chainx = require('chainx.js').default;

var app = express()

async function asyncSendPCX(address) {
    console.log(address);
    // 目前只支持 websocket 链接
    const chainx = new Chainx('wss://chainx.buildlinks.org/');

    // 等待异步的初始化
    await chainx.isRpcReady();

    // 构造交易参数（同步）

    const extrinsic = chainx.asset.transfer(address, 'PCX', '50000', 'chainxFans.org免费水龙头');

    // 查看 method 哈希
    console.log('Function: ', extrinsic.method.toHex());

    return new Promise((resolve, reject) => {
        extrinsic.signAndSend('0x6b45d2b296300314df208839fdcf7dca6bf132fdd4d74177701b9960d2c1f49e', (error, response) => {
            if (error) {
                console.log(error);
                resolve({
                    "status": 0,
                    "msg": error
                });
            } else if (response.status === 'Finalized') {
                if (response.result === 'ExtrinsicSuccess') {
                    console.log('交易成功');
                    let txHash = response.txHash;
                    resolve({
                        "status": 1,
                        "msg": "转账成功",
                        "txHash": txHash
                    });
                }
            }
        });
    })
};

app.set('port', (process.env.PORT || 4000))

app.get('/getfree', async function (req, res) {
    let address = req.query.address;
    let result = await asyncSendPCX(address)
    res.json(result)
})

app.listen(app.get('port'), function () {
    console.log("Node app is running at localhost:" + app.get('port'))
})