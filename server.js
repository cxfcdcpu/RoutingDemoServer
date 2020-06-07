const net = require('net');
const port = 7676;
const host = '0.0.0.0';

const server = net.createServer();
server.listen(port, host,function(){
  console.log('TCP SERVER listening on port 7676!');
});

var sockets = [];
var resultDic = {}; 
var routingDic = {};
var routingDic2 = {};
var connected = false;

server.on('connection', function(sock) {
    console.log('CONNECTED: ' + sock.remoteAddress + ':' + sock.remotePort);
    
    
    if(sock.remoteAddress!='131.151.90.143'){
    
        console.log("Get unexpected tcp connection");
    }
    else{
        sockets.push(sock);
        connected = true;
    }
    sock.on('data', function(data) {
        console.log('DATA ' + sock.remoteAddress + ': ' + data);

        if(connected)sockets[0].write("heartbeats: "+data);
        
        if(data)
        {
            var dataArr=data.toString().split("\n");
            if(dataArr[0].indexOf("0.")!=-1)
            {
              resultDic[dataArr[0].replace(/\s/,"")]=dataArr;
            
            }
        }
        
    });
    sock.on('error', function(ex) {
      console.log("handled error");
      console.log(ex);
    });
    // Add a 'close' event handler to this instance of socket

    sock.on('close', function(data) {
        var index;
        for(index=0;index < sockets.length; index++)
        {
          if(sockets[index].remoteAddress === sock.remoteAddress && sockets[index].remotePort === sock.remotePort)
          {
            break;
          }
        }
        
        if (index !== -1) sockets.splice(index, 1);
        if (index ==0) connected = false;
        console.log('CLOSED: ' + sock.remoteAddress + ' ' + sock.remotePort);
    });


});

//const favicon = require('express-favicon');
var fs = require('fs');
const express=require('express')
bodyParser = require('body-parser')
const app=express()
const spawn= require('child_process').spawn;

app.set('view engine', 'ejs')
app.use(express.static('public'));
//app.use(favicon(__dirname + '/public/favicon.png'));
app.use(bodyParser.json());
app.get('/',function(req,res){
  res.render('main');
});

app.get('/qazxsw',function(req,res){

  res.render('epm');
});

var connectionCounter=0;
app.post('/qazxsw',function(req,res)
{
    connectionCounter++;
    if(typeof sockets[0] === 'undefined') {
        console.log("no client exists");
    }
    else {
        console.log("connection counter: "+connectionCounter);
        sockets[0].write("I'm OK");
    }


});

/*
app.get('/Demo', function(req,res){
  var resultID=req.query.resultID;
    
  if(routingDic[resultID]!=4){
      res.send(0);
  }
  else{
      fs.readFile('./simulation/Users/'+resultID.substr(0,8)+"/debug.txt", 'utf8', function(err, contents) {
          var dataList = contents.split("\n");
          var preT = 0;
          var dataLen = dataList.length;
          var cline = "";
          for(var i = 0; i<dataLen; i++)
          {
            var line = dataList[i].split(" ");
            
              
            if(parseInt(line[2])==111){
              cline+="1:"+line[3];
            }
            else{
              cline+=line[3];  
                
            }
              
            if(line[5] > preT){
              cline+="\n";  
              preT = line[5];
            }
          }
          res.send(cline);
          console.log(dataList.toString());
      });   
      
  }
      

});
*/
app.get('/Demo', function(req,res){
  var resultID=req.query.resultID;
    
  if(routingDic[resultID]!=4){
      console.log("not Exist");
  }
  else{
      console.log("fection data for: "+"./simulation/Users/"+resultID.substr(0,8)+"/debug.txt");
      fs.readFile('./simulation/Users/'+resultID.substr(0,8)+"/debug.txt", 'utf8', function(err, contents) {
          
          
          
          var dataList = contents.split("\n");
          
          var preT = 0;
          var dataLen = dataList.length;
          var cline = "";
          for(var i = 0; i<dataLen; i++)
          { 
            //console.log(dataList[i]);
            var line = dataList[i].split(" ");
            if (line.length == 0)break;
            
            if(line[5] > preT){
              cline+=";";  
              preT = line[5];
            }
              
            if(parseInt(line[2])==111){
              cline+="1:"+line[3]+" ";
            }
            else{
              cline+=line[3]+" ";  
                
            }
              

          }
          res.send(cline);
          
      });   
      
  }
      

});


app.get('/helpFile', function(req,res){
  var tempFile = "./public/tutorial.pdf";
  fs.readFile(tempFile, function (err,data){
    res.contentType("application/pdf");
    res.send(data);
  });
});

app.get('/resetSim', function(req,res){
    var resultID=req.query.resultID;
    if(resultID in routingDic && routingDic[resultID]==4)
    {
        routingDic[resultID]= 2;
    }
});

app.get('/runTOSSIM', function(req,res){
    
    var resultID=req.query.resultID;
    var sourceNode = req.query.sourceNode;
    //console.log("simulating routing for: "+resultID + "from source node: "+ sourceNode);
    
    if(resultID in routingDic && routingDic[resultID]==1)
    {
    
      console.log("Not ready for routing.");
    
    }
    else if(resultID in routingDic && routingDic[resultID]==2)
    {
      
      routingDic[resultID] = 3;
      const gSim=spawn('sh',["./simulation/Users/"+resultID.substr(0,8)+"/runSim.sh", sourceNode, routingDic2[resultID], resultID.substr(0,8) ]);
      console.log("Simulating routing for ID: "+ resultID.substr(0,8));
      
      gSim.on('exit', function (code, signal) {
        if(code==0){routingDic[resultID]=4;}
        console.log('child process exited with code: ' +
                    code + "signal: " + signal);
      });
    
    }
    else if(resultID in routingDic && routingDic[resultID]==3)
    {
    
      console.log("Is simulating, please wait");
    
    }
    else if(resultID in routingDic && routingDic[resultID]==4)
    {
    
      console.log("Done simulation");
      res.send(0);
    
    }    
    //res.send(9);

});


app.get('/getRoutingResult',function(req,res){
  var resultID=req.query.resultID;
  if(resultID in resultDic && resultDic[resultID])
  {
    res.send(resultDic[resultID].slice(1).toString());
    
    if(!(resultID in routingDic))
    {
      routingDic[resultID]=1;
      var rMSG = "[";
      var rInd;
      
      for(rInd = 1 ; rInd < resultDic[resultID].length; rInd++){
        var curMSG = resultDic[resultID][rInd].replace(/(\(|\))/,"").split(";");
        if(curMSG.length == 7)
        {
          var j;
          for(j=0; j<5; j++){
            rMSG += parseInt(curMSG[j]);
            rMSG += ",";
          }
        }      
      }
      rMSG += "255,";
      for(rInd = 1 ; rInd < resultDic[resultID].length; rInd++){
        var curMSG = resultDic[resultID][rInd].replace(/(\(|\))/,"").split(";");
        //console.log(curMSG);
        if(curMSG.length == 5)
        {
          var j;
          for(j=0; j<4; j++){
            rMSG += parseInt(curMSG[j]);
            rMSG += ",";
          }
        }      
      }
      

      rMSG =  rMSG.substr(0,rMSG.length-1) +"]";
      console.log(rMSG);
      routingDic2[resultID]=rMSG;
      //const gsh=spawn('sh',["./simulation/test.sh", resultID.substr(0,8)]);
      const gWSN=spawn('python',["./simulation/generateWSN.py", resultID.substr(0,8)]);
      console.log("generating WSN for ID: "+ resultID.substr(0,8));
      
      gWSN.on('exit', function (code, signal) {
        if(code==0){routingDic[resultID]=2;}
        console.log('child process exited with code: ' +
                    code + "signal: " + signal);
      });
      
      var tempDir = "./simulation/Users/"+resultID.substr(0,8)+"/";
      fs.createReadStream("./simulation/HopVectorBroadcastC.nc").pipe(fs.createWriteStream(tempDir+"HopVectorBroadcastC.nc"));
      fs.createReadStream("./simulation/HopVectorBroadcastAppC.nc").pipe(fs.createWriteStream(tempDir+"HopVectorBroadcastAppC.nc"));
      fs.createReadStream("./simulation/HopVectorBroadcast.h").pipe(fs.createWriteStream(tempDir+"HopVectorBroadcast.h"));
      fs.createReadStream("./simulation/Makefile").pipe(fs.createWriteStream(tempDir+"Makefile"));
      fs.createReadStream("./simulation/MySimulation.py").pipe(fs.createWriteStream(tempDir+"MySimulation.py"));
      fs.createReadStream("./simulation/SimHelper.py").pipe(fs.createWriteStream(tempDir+"SimHelper.py"));
      fs.createReadStream("./simulation/runSim.sh").pipe(fs.createWriteStream(tempDir+"runSim.sh"));
      fs.createReadStream("./simulation/universal_functions_new.h").pipe(fs.createWriteStream(tempDir+"universal_functions_new.h"));
    }
    else{
      console.log("Already on processing routing simulation");
    }
  }
});



app.post('/findConstraints',function(req,res)
{
    var data=req.body.draw;
    var total=req.body.total;
    var myId=req.body.me;
    var epoch=req.body.ep;
    var i = 0;
    var temp="";
    var hash=0;
    console.log("total: "+total);
    
    for( i=0;i<2*total;i++)
    {
        var x1=parseInt(data[i++]);
        var y1=parseInt(data[i]);
        var buf=[];
        buf.push('\n*****');
        buf.push(myId);
        buf.push(epoch);    
        buf.push(3);
        buf.push(i/2);
        buf.push(x1);
        buf.push(y1);
        buf.push('*****\n');
        temp+=buf.join();
        hash+=x1;
        hash+=y1;
    }
    
    hash=0;
    for( i=0;i<2*total;i++)
    {
        var x1=parseInt(data[i++]);
        var y1=parseInt(data[i]);
        var buf=[];
        buf.push('\n*****');
        buf.push(myId);
        buf.push(epoch);    
        buf.push(3);
        buf.push(i/2);
        buf.push(x1);
        buf.push(y1);
        buf.push('*****\n');
        temp+=buf.join();
        hash+=x1;
        hash+=y1;
    }
    
    if(hash>0)
    {
        res.send(hash.toString());
        var buf=[];
        
        if(typeof sockets[0] === 'undefined') {
            console.log("no client exists");
        }
        else {
            console.log("Sending "+myId+"'s data, epoch "+epoch+". Total size: "+ temp.length);
            sockets[0].write(temp);
        }
        
        if(typeof sockets[0] === 'undefined') {
            console.log("no client exists");
        }
        else {
            console.log("Sending "+myId+"'s data, epoch "+epoch+". Total size: "+ temp.length);
            sockets[0].write(temp);
        }
        var buf=[];
        buf.push('\n*****');
        buf.push(myId);
        buf.push(epoch);    
        buf.push(4);
        buf.push(hash)
        buf.push(parseInt(total));
        buf.push(0);
        buf.push('*****\n');
        temp+=buf.join();
        if(typeof sockets[0] === 'undefined') {
            console.log("no client exists");
        }
        else {
            console.log("Sending "+myId+"'s data, epoch "+epoch+". Total size: "+ temp.length);
            sockets[0].write(temp);
        }
        if(typeof sockets[0] === 'undefined') {
            console.log("no client exists");
        }
        else {
            console.log("Sending "+myId+"'s data, epoch "+epoch+". Total size: "+ temp.length);
            sockets[0].write(temp);
        }
    
    
    }


});


app.post('/',function(req,res)
{
  
  var myId=req.body.me;
  var total=req.body.total;
  var anchor = req.body.anchor;
  var data=req.body.nodes;
  var epoch=req.body.ep;
  var rg=req.body.range;
  
  
  var temp;
  var buf=[];
  buf.push('\n*****');
  buf.push(myId);
  buf.push(epoch);
  buf.push(0);
  buf.push(total);
  buf.push(anchor);
  buf.push(rg);
  buf.push('*****\n');
  temp+=buf.join();

  var buf=[];
  buf.push('\n*****');
  buf.push(myId);
  buf.push(epoch);
  buf.push(0);
  buf.push(total);
  buf.push(anchor);
  buf.push(rg);
  buf.push('*****\n');
  temp+=buf.join();
  
  var i=0;
  var counter=0;
  
  for(i=0;i<anchor;i++){
  
    var buf=[];
    buf.push('\n*****');
    buf.push(myId);
    buf.push(epoch);
    buf.push(1);
    buf.push(counter++);
    buf.push(data[2*i]);
    buf.push(data[2*i+1]);
    buf.push('*****\n');
    temp+=buf.join();

  }
  counter=0;
  i=0;
  var tempNode=""+total+" "+anchor+" "+rg;
  while(i<total){
    var buf=[];
    buf.push('\n*****');
    buf.push(myId);
    buf.push(epoch);
    buf.push(1);
    buf.push(counter++);
    buf.push(data[2*i]);
    buf.push(data[2*i+1]);
    tempNode+="\n"+data[2*i];
    tempNode+=" ";
    tempNode+=data[2*i+1];
    i++;
    buf.push('*****\n');
    temp+=buf.join();

  }
  var dir = "./simulation/Users/"+myId;
  if(!fs.existsSync(dir)){
    fs.mkdirSync(dir);
  }
  
  fs.writeFile(dir+"/graph.txt", tempNode, function (err) {
    if (err) throw err;
    console.log('Saved!');
  }); 
  

  
  
  counter=total-100;
  i=total-100;
  while(i<total){
    var buf=[];
    buf.push('\n*****');
    buf.push(myId);
    buf.push(epoch);
    buf.push(1);
    buf.push(counter++);
    buf.push(data[2*i]);
    buf.push(data[2*i+1]);
    
    i++;
    buf.push('*****\n');
    temp+=buf.join();

  }
  


    if(typeof sockets[0] === 'undefined') {
        console.log("no client exists");
    }
    else {
        console.log("Sending "+myId+"'s data, epoch "+epoch+". Total size: "+ temp.length);
        sockets[0].write(temp);
    }

});
  
app.listen(7780,function(){
  console.log('Example app listening on port 7780!');
});
