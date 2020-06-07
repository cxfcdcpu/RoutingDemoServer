//array that hold nodes x position, starts empty
var nodesX = [];
//array that hold nodes y position, starts empty
var nodexY = [];
//array that hold anchor node positions. 0 = not anchor nodes, 1 = is anchor nodes
var anchorNodes = [];
var requestList=[];
var requestInd=-1;
var requestResult = {};
var curInd=-1;
var constraints = [];

//array holding information to be displayed in text box
var information = new Array(25);
//contains the position of array that is shown in text field
var currTextFieldPos = 0;


var myID=Math.random().toString().substring(0,8);
var epoch=0;
//JSON object holding drawing info
var jsonDraw = {
    me:myID,
    ep: epoch,
    total : 0,
    draw: []
};

var jsonNodes = {
        me: myID,
        ep: epoch,
        range: 0,
        total: 0,
        anchor: 0,
        nodes: []
};

//boolean to control if drawing is enabled. Starts false, enables when pen button is clicked
var toggleDraw = false;
//boolean to control if hopinfo is enabled. starts false, enables when hopinfo button is clicked
var toggleHopInfo = false;
var visualSim = false;
var selectSource = false;

//boolean flag determining if user is drawing. originally, false
var flag = false;
//previous and current positions of mouse, maintined to draw properly
var prevX = 0;
var currX = 0;
var prevY = 0;
var currY = 0;
var dot_flag = false;


//response from server
var isResponse = false;
var loading;

//resizes canvas size
function resizeCanvas() {
    /*
    //resize the width of canvas
    document.getElementById("canvas").width = window.innerWidth - 20;
    //resize the height of canvas
    document.getElementById("canvas").height = window.innerHeight - 55;
    */
    document.getElementById("canvas3").width = document.getElementById("sensorFieldWidthSlider").value;
    document.getElementById("canvas3").height = document.getElementById("sensorFieldLengthSlider").value;
    document.getElementById("canvas2").width = document.getElementById("sensorFieldWidthSlider").value;
    document.getElementById("canvas2").height = document.getElementById("sensorFieldLengthSlider").value;
    document.getElementById("canvas").width = document.getElementById("sensorFieldWidthSlider").value;
    document.getElementById("canvas").height = document.getElementById("sensorFieldLengthSlider").value;
    document.getElementById("penButton").style.background = "#BFF792";
    document.getElementById("genWSNsButton").style.background = "#BFF792";
    document.getElementById("routingMSG").style.background = "#F8E78F";
    document.getElementById("visualizeRouting").style.background = "#F8E78F";
}

//opens modal Generate WSNs
function openGenerateWSNs() {
    document.getElementById("generateWSNsModal").style.display="block";
}

//closes model Generate WSNs
function closeGenerateWSNs() {
    document.getElementById("generateWSNsModal").style.display="none";
}

//closes loading bar modal
function closeLoadingBar() {
  document.getElementById("loadingBarModal").style.display="none";
  clearInterval(loading);
  
}

//closes searching WSNs modal
function closeSearchingWSNs() {
    document.getElementById("searchingWSNsModal").style.display = "none";
}

//closes search nodes modal
function closeSearchNodes() {
	document.getElementById("searchNodesModal").style.display = "none";
}

//get value of penWidth
function penWidthGetValue() {
    document.getElementById("penWidthValue").innerHTML = document.getElementById("penWidthSlider").value;
}

//get value of nodes in network slider
function nodesInNetworkGetValue() {
    document.getElementById("nodesInNetworkValue").innerHTML = document.getElementById("nodesInNetworkSlider").value;
}

//get value of anchors in network slider
function anchorsInNetworkGetValue() {
    document.getElementById("anchorsInNetworkValue").innerHTML = document.getElementById("anchorsInNetworkSlider").value;
}
//get value of radio range slider
function radioRangeGetValue() {
    document.getElementById("radioRangeValue").innerHTML = document.getElementById("radioRangeSlider").value;
}
//get value of sensor field width slider
function sensorFieldWidthGetValue() {
    document.getElementById("sensorFieldWidthValue").innerHTML = document.getElementById("sensorFieldWidthSlider").value;
}

//get value of sensor field length slider
function sensorFieldLengthGetValue() {
    document.getElementById("sensorFieldLengthValue").innerHTML = document.getElementById("sensorFieldLengthSlider").value;
}

//closes popup
function closePopUp() {
    document.getElementById("popup").style.display = "none";
}

function disableDrawing(){
    toggleDraw = false;
    //changes color of button to show that toggleDraw is false/offdsfd
    document.getElementById("penButton").style.background = "#BFF792";
}

function disableHopInfo(){
		toggleHopInfo = false;
		//if toggleHopInfo is not false, then it is true, change toggleHopInfo to false
		document.getElementById("hopInfoButton").removeAttribute("style");

}



//changes toggleDraw to true or false depending on button click
function toggleDrawing() {
    disableHopInfo();
    selectSource = false;
    //if toggleDraw is false then changes toggleDraw to true
    if(toggleDraw == false) {
        toggleDraw = true;
        //change color of button to show that toggleDraw is true/on
        document.getElementById("penButton").style.background = "#FF0000";
    }
    //if toggleDraw is not false then it is true, change toggleDraw to false
    else {
        toggleDraw = false;
        //changes color of button to show that toggleDraw is false/off
        document.getElementById("penButton").style.background = "#BFF792";
    }
}

//changes toggleHopInfo to true or false depending on button click
function toggleHopInfoing() {
  disableDrawing();
  selectSource = false;
	//if toggleHopInfo is false then changes to true
	if(toggleHopInfo == false) {
		toggleHopInfo = true;
		//change color of button to show that toggleHopInfo is true/on
		document.getElementById("hopInfoButton").style.background = "#FF0000";
	}
	else {
		toggleHopInfo = false;
		//if toggleHopInfo is not false, then it is true, change toggleHopInfo to false
		document.getElementById("hopInfoButton").removeAttribute("style");
	}
}

//reset variables from generateNodes
function resetGenerateNodes() {
    //reset nodesX and nodesY array
    nodesX = [];
    nodesY = [];
    anchorNodes=[];
        //reset json object
    jsonDraw = {
        me:myID,
        ep: epoch,
        total : 0,
        draw: []
    };
    
    //reset anchorNodes. 0 = not anchor nodes, 1 = is anchor nodes
    for(var i = 0; i < document.getElementById("anchorsInNetworkSlider").value; i++) {
        //change current position of array to 0
        anchorNodes.push(1);
    }
    //determine anchorNodes. # of anchor nodes determined by slider in Generate WSNs

    //reset jsonNodes

     jsonNodes.range=0;
     jsonNodes.total=0;
     jsonNodes.anchor=0;
     jsonNodes.nodes=[];
    //closes popup boxes
    information = new Array(25);
    constraints = [];
    document.getElementById("popup").style.display = "none";
}

function euDis(x1,y1,x2,y2){
  return (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2);
}

//generate nodes
function generateNodes() {
    //get # of nodes from Generate WSNs
    var numNodes = document.getElementById("nodesInNetworkSlider").value;
    //get X value of canvas from Generate WSNs
    var maxX = document.getElementById("sensorFieldWidthSlider").value;
    //get Y value of canvas from Generate WSNs
    var maxY = document.getElementById("sensorFieldLengthSlider").value;

    //loops until length of nodes = numNodes
    //generates x and y coordinates of nodes
    while(nodesX.length < numNodes && nodesY.length < numNodes) {
        //generate random x (0 - maxX.length)
        var ranX = Math.floor(Math.random() * maxX);
        //generate random y (0 - maxY.length)
        var ranY = Math.floor(Math.random() * maxY);

        //check to see if combination of x and y positions are duplicates
        //nodesX and nodesY are/should be same length, checking either length is enough
        //counter for for loop
        var i = 0;
        for(i = 0; i < nodesX.length; i++) {
            //if position is duplicate
            if(euDis(nodesX[i], nodesY[i] , ranX, ranY)<25) {
                //break out for loop
                break;
            }
        }

        //if i is = to nodesX or nodesY length then that means for loop reached end of arrays, meaning no duplicates
        if(i == nodesX.length) {
            //add generates x and y to position of nodes
            nodesX.push(ranX);
            nodesY.push(ranY);
        }
    }
}

//place generated nodes on canvas
function placeNodesOnCanvas() {
    //get canvas element from html
    var canvas = document.getElementById("canvas");
    //canvas is 2d
    var ctx = canvas.getContext("2d");

    //change opacity of canvas
    canvas.style.opacity = 1;
    
    //loops through length of nodesX and nodesY array
    for(var i = 0; i < nodesX.length; i++) {
        //if current node is an anchor node
        if(anchorNodes[i] == 1) {
            //change color of nodes to red
            ctx.fillStyle = "#FF0000";   
            
                    //place nodes on canvas
        //ctx.fillRect(nodesX[i], nodesY[i], 5, 5);
        ctx.beginPath();
        ctx.lineWidth = 1;
        ctx.arc(nodesX[i], nodesY[i], 2, 0, 2 * Math.PI);
        ctx.stroke();
        ctx.fill();
        ctx.closePath();
        }
        //if current node is not an anchor node
        else {
            //change color of nodes to black
            ctx.fillStyle = "#000000";
            
                    //place nodes on canvas
        //ctx.fillRect(nodesX[i], nodesY[i], 5, 5);
        ctx.beginPath();
        ctx.lineWidth = 1;
        ctx.arc(nodesX[i], nodesY[i], 1, 0, 2 * Math.PI);
        ctx.stroke();
        ctx.fill();
        ctx.closePath();
        }
        //console.log("done place");
    }
    //makes current canvas drawing into an image and changes source of image tag
    document.getElementById("canvasImage").src = canvas.toDataURL();
        
    //changes opacity of canvas
    canvas.style.opacity = 0.25;
    console.log("done place"); 
    setTimeout(function(){
      closeGenerateWSNs();
    },500);   


//creates json with node information
    jsonNodes.ep=epoch++;
    jsonNodes.range=document.getElementById("radioRangeSlider").value;
    //loops through nodesX / nodesY
    var counter=0;
    for(var i = 0; i < nodesX.length; i++) {
        //variable containing data if current node is an anchor, default is false.
        var isAnchor = false;

        //determine if current node i is an anchor node
        if(anchorNodes[i] == 1) {
            //current node is anchor
            isAnchor = true;
            counter+=1;
        }

        //push data into jsonNodes
        jsonNodes.nodes.push( parseInt(nodesX[i]));
        jsonNodes.nodes.push( parseInt(nodesY[i]));
    }
    jsonNodes.total=nodesX.length;
    jsonNodes.anchor=counter;
    //console.log(jsonNodes);
    $.ajax({
        type: 'post',
        data: JSON.stringify(jsonNodes),
        contentType: 'application/json',
        dataType: 'json'
    });

}

function hideCanvas() {
  document.getElementById("canvasImage").style.display = "none";
  document.getElementById("canvas").style.display = "none";
  document.getElementById("canvas2").style.display = "none";
}

function showCanvas() {
  document.getElementById("canvasImage").style.display = "block";
  document.getElementById("canvas").style.display = "block";
  document.getElementById("canvas2").style.display = "block";
}

//tracks mouse movement
function trackMouse() {
    var canvas = document.getElementById("canvas");

    //track the users mouse and actions
    canvas.addEventListener("mousemove", function (e) {
        findXY("move", e);
    }, false);
    canvas.addEventListener("mousedown", function (e) {
        findXY("down", e);
    }, false);
    canvas.addEventListener("mouseup", function (e) {
        findXY("up", e);
		//if toggleHopInfo is true
		if(toggleHopInfo == true) {
			displayHopInfo(e);
		}
		if(selectSource == true) {
      requestRoutingSim(e);
    }
    }, false);
    
    
    canvas.addEventListener("mouseout", function (e) {
        findXY("out", e);
    }, false);
}

//finds x and y coordinate of mouse
function findXY(action, e) {
    if(toggleDraw == true) {
        var canvas = document.getElementById("canvas");
        var ctx = canvas.getContext("2d");

        //changes opacity of line
        ctx.globalAlpha = 0.2;
        
        //if user mouse is down
        if(action == "down") {
            //change prev x and y locations to current x and y locations
            prevX = currX;
            prevY = currY;
            currX = e.clientX - canvas.getBoundingClientRect().left;
            currY = e.clientY - canvas.getBoundingClientRect().top;
            //drawing is true, flag is true
            flag = true;
            dot_flag = true;

            //starting position of drawing/line
            if(dot_flag == true) {
                //start drawing
                ctx.beginPath();
                ctx.fillRect(currX, currY, 1, 1);
                //add starting point to json object
                jsonDraw.ep=epoch++;
                jsonDraw.total+=2;
                jsonDraw.draw.push(-123);
                jsonDraw.draw.push(document.getElementById("penWidthSlider").value);
                jsonDraw.draw.push(parseInt(currX));
                jsonDraw.draw.push(parseInt(currY));
                dot_flag = false;
            }
        }

        //if user lifts up mouse button or leaves canvas, stop drawing
        if (action == "up" || action == "out") {
            flag = false;
			ctx.closePath();
        }

        //if user moves mouse, draw lines from starting point
        if (action == "move") {
            if(flag == true) {
                prevX = currX;
                prevY = currY;
                currX = e.clientX - canvas.getBoundingClientRect().left;
                currY = e.clientY - canvas.getBoundingClientRect().top;
                draw();
            }
        }
    }
}


function randomTest(){
  erase();
  var c1,c2,h1,h2,d;
  var dis;
  do
  {
    c1=Math.floor(Math.random() * jsonNodes.anchor); 
    c2=0;
    do{
      c2=Math.floor(Math.random() * jsonNodes.anchor);
    }while(c2==c1);
    
    h1=Math.floor(Math.random() * 10)+3;
    h2=0;
    do{
      h2=Math.floor(Math.random() * 10)+3;
    }while(h2==h1); 
    
    d=Math.floor(Math.random() * 50)+30;
    dis=(nodesX[c1]-nodesX[c2])*(nodesX[c1]-nodesX[c2])+(nodesY[c1]-nodesY[c2])*(nodesY[c1]-nodesY[c2]);
  }while(dis>(h1+h2)*(h1+h2)*d*d)
  
  var canvas = document.getElementById("canvas");
  var ctx = canvas.getContext("2d");
  ctx.beginPath();
  ctx.arc(nodesX[c1], nodesY[c1], h1*d, 0, 2 * Math.PI);
  ctx.stroke(); 
  ctx.beginPath();
  ctx.arc(nodesX[c1], nodesY[c1], h1*d-d, 0, 2 * Math.PI);
  ctx.stroke(); 
  ctx.beginPath();
  ctx.arc(nodesX[c2], nodesY[c2], h2*d, 0, 2 * Math.PI);
  ctx.stroke(); 
  var i,j;
  var ccc=0;
  for(i=0;i<2000;i++)
  {
    for(j=0;j<2000;j++)
    {
      if(pDis(i,j,nodesX[c2],nodesY[c2])<h2*h2*d*d && pDis(i,j,nodesX[c1],nodesY[c1])<h1*h1*d*d && pDis(i,j,nodesX[c1],nodesY[c1])>(h1-1)*(h1-1)*d*d)
        ccc+=1;
        if(i%4==0&&j%4==0) {
		  ctx.fillStyle = "#FF0000";
		  ctx.fillRect(i,j,1,1);
	    }
    }
  }
  
  console.log(ccc);
}


function randomTest2(){
  erase();
  var c1,c2,c3,ah,h3,d1,d2;
  var dis;
  do
  {
    c1=Math.floor(Math.random() * jsonNodes.anchor); 
    c2=0;
    do{
      c2=Math.floor(Math.random() * jsonNodes.anchor);
    }while(c2==c1);
    ah=Math.floor(Math.random() * 10)+1;

    c3=Math.floor(Math.random() * jsonNodes.anchor); 
    h3=Math.floor(Math.random() * 7)+1;


    d1=Math.floor(Math.random() * 50)+30;
    d2=Math.floor(Math.random() * 50)+30;
    dis=(nodesX[c1]-nodesX[c2])*(nodesX[c1]-nodesX[c2])+(nodesY[c1]-nodesY[c2])*(nodesY[c1]-nodesY[c2]);
    
  }while(dis < 4*ah*ah*d1*d1);
  var canvas = document.getElementById("canvas");
  var ctx = canvas.getContext("2d");
  ctx.beginPath();
  ctx.arc(nodesX[c3], nodesY[c3], h3*d2, 0, 2 * Math.PI);
  ctx.stroke(); 
  var i,j;
  var ccc=0;
  for(i=0;i<2000;i++)
  {
    for(j=0;j<2000;j++)
    {
      if(pDis(i,j,nodesX[c3],nodesY[c3])<h3*h3*d2*d2 && 
        Math.sqrt(pDis(i,j,nodesX[c1],nodesY[c1]))-Math.sqrt(pDis(i,j,nodesX[c2],nodesY[c2]))<2*ah*d1 && 
        Math.sqrt(pDis(i,j,nodesX[c1],nodesY[c1]))-Math.sqrt(pDis(i,j,nodesX[c2],nodesY[c2]))>2*(ah-1)*d1 )
        {
            ccc+=1;
            if(i%4==0&&j%4==0) {
		      ctx.fillStyle = "#FF0000";
		      ctx.fillRect(i,j,1,1);
		      }
	    }
	    
	  if(Math.abs(Math.sqrt(pDis(i,j,nodesX[c1],nodesY[c1]))-Math.sqrt(pDis(i,j,nodesX[c2],nodesY[c2]))-2*ah*d1)<2 ||
        Math.abs(Math.sqrt(pDis(i,j,nodesX[c1],nodesY[c1]))-Math.sqrt(pDis(i,j,nodesX[c2],nodesY[c2]))-2*(ah-1)*d1)<2 )
      {
            ctx.fillRect(i,j,1,1);
      
      }
    }
  }
  if(ccc>0)alert(nodesX[c1]+" "+nodesY[c1]+" "+nodesX[c2]+" "+nodesY[c2]+" "+nodesX[c3]+" "+nodesY[c3]+" "+ah+" "+h3+" "+d1+" "+d2+" "+ccc);
  console.log(ccc);
}





function pDis(x1,y1,x2,y2)
{
  return (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2);
}
//allows the user to draw on canvas
function draw() {
    var canvas = document.getElementById("canvas");
    var ctx = canvas.getContext("2d");
    
    //changes opacity of line
    ctx.globalAlpha = 0.5;
    
    //start drawing
    ctx.moveTo(prevX, prevY);
    ctx.lineTo(currX, currY);
    jsonDraw.total+=1;
    jsonDraw.draw.push( currX);
    jsonDraw.draw.push( currY);
    ctx.lineWidth = document.getElementById("penWidthSlider").value;
	ctx.lineJoin = "round";
	ctx.lineCap = "round";
    ctx.strokeStyle = document.getElementById("color").value;
    ctx.stroke();
}

function erase3(){

    var canvas3 = document.getElementById("canvas3");
    var ctx3 = canvas3.getContext('2d');
    ctx3.clearRect(0, 0, canvas3.width, canvas3.height);

}

function erase2(){

    var canvas2 = document.getElementById("canvas2");
    var ctx2 = canvas2.getContext('2d');
    //reset global alpha
    ctx2.globalAlpha = 1;
    //reset global composite operation
    ctx2.globalCompositeOperation = "source-over";
    //clear canvas
    ctx2.clearRect(0, 0, canvas2.width, canvas2.height);
    
}

//erases everything in canvas then places generated nodes back on canvas
function erase() {
    var canvas = document.getElementById("canvas");
    var ctx = canvas.getContext('2d');
    //reset global alpha
    ctx.globalAlpha = 1;
    //reset global composite operation
    ctx.globalCompositeOperation = "source-over";
    //clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    erase2();
    
    
    //reset json object
    jsonDraw = {
        me:myID,
        ep: epoch,
        total : 0,
        draw: []
    };
    //resets canvas images
    document.getElementById("canvasImage").src = "";
    //place nodes back on canvas
    placeNodesOnCanvas();
}

//clears entire canvas
function clearCanvas() {
    //resets all variables
    resetGenerateNodes();
    erase();
}




//displays hopinfo
function displayHopInfo(e) {
	//obtain current x and y positions of mouse
    currX = e.clientX - canvas.getBoundingClientRect().left;
    currY = e.clientY - canvas.getBoundingClientRect().top;

	//loop through nodesX array to determine if current mouse location is a node
	for(var i = 0; i < nodesX.length; i++) {
		//check to see if current mouse x position is in nodesX array
		if(euDis(currX,currY, nodesX[i],nodesY[i])< 9){
			//check to see if current Y position is in nodesY array
			
                var popupBox = document.getElementById("popup");
                popupBox.style.display = "block";
                popupBox.style.top = currY;
                popupBox.style.left = currX;
                if(anchorNodes[i]==1){popupBox.style.backgroundColor="red";}
                else{
                  popupBox.style.backgroundColor="silver";
                }
                popupBox.innerHTML = "Node #: " + i + "<br />" + "X: " + nodesX[i] + "<br />" + "Y: " + nodesY[i];
			
		}
	}
}


function findConstraints(){


  $.ajax({
      type: 'post',
      url: 'findConstraints',
      data: JSON.stringify(jsonDraw),
      contentType: 'application/json',
      dataType: 'json',
      success:function(data) {
        requestList.push(data);
        console.log("request ID: "+data);
        requestInd+=1;
        curInd=requestInd;
      }
  });
}

//displays loading bar and wait to receive data from server
function waitForResponseFromServer() {
    
    if(jsonDraw.total==0 || jsonNodes.total==0){
      alert("Please generate the WSNs and draw the trajectory first.");
      return;
    }
    document.getElementById("loadingBarModal").style.display="block";
    //progress bar variables
    var loadingBar = document.getElementById("loadingBar");
    var progressBar = document.getElementById("progressBar");
    //timer is 2min, 120,000ms = 2min
    const timer = 120000;
    //reset isResponse
    isResponse = false;
    var loadingBarPercent = 1;
    //temp count
    var count = 0;
    loadingBar.style.display = "block";
    progressBar.style.display = "block";
    curInd=-1;
    findConstraints();
    document.getElementById("loadingBarMessage").innerHTML = "Processing your trajectory encoding in the remote server, Please wait.";
    //loading = setInterval(updateLoadingBar , 100);
    
    loadingBar.style.width = 0 + '%';
    var call =function(){
        //console.log("reach call");
        var st="-1";
        if(curInd!=-1)
        {
          st=requestList[curInd].toString();
        }
        var u;
        $.ajax({
            url: 'getRoutingResult?resultID='+myID.toString()+st,
            type: 'get',
            timeout: 2000,
            error: function(x, textStatus, m) {
                //console.log("reach error");
                
                if (textStatus=="timeout") {
                   if(loadingBarPercent >= 100||st==0)
                   {
                     document.getElementById("loadingBarMessage").innerHTML = "Unable to receive response from server. Please try again";
                   }
                   else
                   {
                     call();
                   }
                   loadingBarPercent = loadingBarPercent + 0.5;
                   loadingBar.style.width = loadingBarPercent + '%';
                }
            },
            success:function(data) {
              loadingBar.style.width = 100 + '%';
              document.getElementById("loadingBarMessage").innerHTML = "Received data from server. Please close window";
              console.log(data);
              constraints = data.split(",");
              information = [];
              var j;
              for (j=0; j < constraints.length; j++)
              {
                information[j]=constraints[j];
              }
              
              setTimeout(function(){
                  closeLoadingBar();
              }, 1000);
              
            }
        });
    };
    
    call();

}


//displays a box with various info when Search WSNs is clicked
function searchWSNs(mode) {  
    var cLen = constraints.length;
    //if mode = start then initiialize text field and populate array information
    if(mode == "start") {
        //rest current position of array that is displayed in text field
        currTextFieldPos = 0;
        //reset array
        //information = [];
        information[cLen]="End, total number of constraints: "+cLen;
        //displays modal/popup
        document.getElementById("searchingWSNsModal").style.display="block";
        
        //code to get information and populate it
        //HERE
        
        //populate text field with the value at position in array 
        document.getElementById("message").value = information[currTextFieldPos];
    }
    //if moving left in array
    else if(mode == "left") {
        //if current position of array that is displayed in text field is 0 then loop to end of array
        if(currTextFieldPos == 0) {
            //set current position to end of array
            currTextFieldPos = cLen;
        }
        //else if current position of array that is displayed in text field is not 0
        else {
            currTextFieldPos--;
        }
        //populate text field with the value at position in array 
        document.getElementById("message").value = information[currTextFieldPos];
    }
    //if moving right in array
    else if(mode == "right") {
        //if current position of array that is displayed in text field is at end of array loop back to beginning of array (0)
        if(currTextFieldPos == cLen) {
            //set current position to end of array
            currTextFieldPos = 0;
        }
        //else if current position of array that is displayed in text field is not at end of array
        else {
            currTextFieldPos++;
        }
        //populate text field with the value at position in array 
        document.getElementById("message").value = information[currTextFieldPos];
    }
}
//when display current area button is pressed
function displayCurrentConstraint() {
    var ds=information[currTextFieldPos].toString().split(";");
    if(ds.length == 5)
    {
      drawCycle(information[currTextFieldPos]);
    }
    if(ds.length == 7)
    {
      drawHyper(information[currTextFieldPos]);
    }
    document.getElementById("searchingWSNsModal").style.display = "none";
    setTimeout(function(){
      document.getElementById("searchingWSNsModal").style.display = "block";
    },2000);
    
}



function drawCycle(data){
  var c1,c2,h1,h2,d;
  var ds=data.toString().substring(1,data.toString().length-1).split(";");
  c1=parseInt(ds[0]);
  c2=parseInt(ds[1]);
  h1=parseInt(ds[2]);
  h2=parseInt(ds[3]);
  d =parseFloat(ds[4]);
  
  var canvas2 = document.getElementById("canvas2");
  var ctx2 = canvas2.getContext("2d");
  canvas2.style.opacity = 1;
  ctx2.globalAlpha = 1;
  ctx2.strokeStyle = "#000000";
  ctx2.lineWidth=1;
  ctx2.beginPath();
  ctx2.arc(nodesX[c1], nodesY[c1], h1*d, 0, 2 * Math.PI);
  ctx2.stroke(); 
  ctx2.beginPath();
  ctx2.arc(nodesX[c1], nodesY[c1], h1*d-d, 0, 2 * Math.PI);
  ctx2.stroke(); 
  ctx2.beginPath();
  ctx2.arc(nodesX[c2], nodesY[c2], h2*d, 0, 2 * Math.PI);
  ctx2.stroke(); 
  

  
  var i,j,kk;
  var ccc=0;
  for(i=0;i<2000;i++)
  {
    for(j=0;j<2000;j++)
    {
    
      if(pDis(i,j,nodesX[c2],nodesY[c2])<h2*h2*d*d && pDis(i,j,nodesX[c1],nodesY[c1])<h1*h1*d*d && pDis(i,j,nodesX[c1],nodesY[c1])>(h1-1)*(h1-1)*d*d)
      {
        ccc+=1;
        if(i%4==0&&j%4==0) {
			    ctx2.fillStyle = "#FF0000";
			    ctx2.strokeStyle = "#FF0000";
			    ctx2.fillRect(i,j,1,1);
		    }      
      }
    }
  }
  
  console.log(ccc);
}

function drawCycle2(data){
  var c1,c2,h1,h2,d;
  var ds=data.toString().substring(1,data.toString().length-1).split(";");
  c1=parseInt(ds[0]);
  c2=parseInt(ds[1]);
  h1=parseInt(ds[2]);
  h2=parseInt(ds[3]);
  d =parseFloat(ds[4]);
  
  var canvas2 = document.getElementById("canvas2");
  var ctx2 = canvas2.getContext("2d");
  canvas2.style.opacity = 1;
  ctx2.globalAlpha = 1;

  var i,j,kk;
  var ccc=0;
  for(i=0;i<2000;i++)
  {
    for(j=0;j<2000;j++)
    {
    
      if(pDis(i,j,nodesX[c2],nodesY[c2])<h2*h2*d*d && pDis(i,j,nodesX[c1],nodesY[c1])<h1*h1*d*d && pDis(i,j,nodesX[c1],nodesY[c1])>(h1-1)*(h1-1)*d*d)
      {
        ccc+=1;
        if(i%4==0&&j%4==0) {
			    ctx2.fillStyle = "#FF0000";
			    ctx2.strokeStyle = "#FF0000";
			    ctx2.fillRect(i,j,2,2);
		    }      
      }
    }
  }
  
  console.log(ccc);
}

function drawHyper(data){
  var c1,c2,c3,ah,h3,d1,d2;
  var ds=data.toString().substring(1,data.toString().length-1).split(";");
  c1=parseInt(ds[0]);
  c2=parseInt(ds[1]);
  c3=parseInt(ds[2]);
  ah=parseInt(ds[3]);
  h3 =parseInt(ds[4]);
  d1 = parseFloat(ds[5]);
  d2 = parseFloat(ds[6]);
  
  var canvas2 = document.getElementById("canvas2");
  var ctx2 = canvas2.getContext("2d");
  
  canvas2.style.opacity = 1;
  ctx2.globalAlpha = 1;
  ctx2.strokeStyle = "#000000";
  ctx2.lineWidth=1;
  ctx2.beginPath();
  ctx2.arc(nodesX[c3], nodesY[c3], h3*d2, 0, 2 * Math.PI);
  ctx2.stroke(); 
  
  var i,j;
  var ccc=0;
  for(i=0;i<2000;i++)
  {
    for(j=0;j<2000;j++)
    {
      if(pDis(i,j,nodesX[c3],nodesY[c3])<h3*h3*d2*d2 && 
        Math.sqrt(pDis(i,j,nodesX[c1],nodesY[c1]))-Math.sqrt(pDis(i,j,nodesX[c2],nodesY[c2]))<2*ah*d1 && 
        Math.sqrt(pDis(i,j,nodesX[c1],nodesY[c1]))-Math.sqrt(pDis(i,j,nodesX[c2],nodesY[c2]))>2*(ah-1)*d1 )
        {
            ccc+=1;
            if(i%4==0&&j%4==0) {
		          ctx2.fillStyle = "#FF0000";
		          ctx2.fillRect(i,j,1,1);
		        }
	      }
	    
	    if(Math.abs(Math.sqrt(pDis(i,j,nodesX[c1],nodesY[c1]))-Math.sqrt(pDis(i,j,nodesX[c2],nodesY[c2]))-2*ah*d1)<2 ||
          Math.abs(Math.sqrt(pDis(i,j,nodesX[c1],nodesY[c1]))-Math.sqrt(pDis(i,j,nodesX[c2],nodesY[c2]))-2*(ah-1)*d1)<2 )
      {
            ctx2.fillRect(i,j,1,1);
      
      }
    }
  }
  
  console.log(ccc);
}

function drawHyper2(data){
  var c1,c2,c3,ah,h3,d1,d2;
  var ds=data.toString().substring(1,data.toString().length-1).split(";");
  c1=parseInt(ds[0]);
  c2=parseInt(ds[1]);
  c3=parseInt(ds[2]);
  ah=parseInt(ds[3]);
  h3 =parseInt(ds[4]);
  d1 = parseFloat(ds[5]);
  d2 = parseFloat(ds[6]);
  
  var canvas2 = document.getElementById("canvas2");
  var ctx2 = canvas2.getContext("2d");
  
  canvas2.style.opacity = 1;
  ctx2.globalAlpha = 1;

  
  
  
  var i,j;
  var ccc=0;
  if(ah>0)
  {
    for(i=0;i<2000;i++)
    {
      for(j=0;j<2000;j++)
      {
        if(pDis(i,j,nodesX[c3],nodesY[c3])<h3*h3*d2*d2 && 
          Math.sqrt(pDis(i,j,nodesX[c1],nodesY[c1]))-Math.sqrt(pDis(i,j,nodesX[c2],nodesY[c2]))<2*ah*d1 && 
          Math.sqrt(pDis(i,j,nodesX[c1],nodesY[c1]))-Math.sqrt(pDis(i,j,nodesX[c2],nodesY[c2]))>2*(ah-1)*d1 )
          {
              ccc+=1;
              if(i%4==0&&j%4==0) {
		            ctx2.fillStyle = "#FF0000";
		            ctx2.fillRect(i,j,2,2);
		          }
	        }
	      
      }
    }
  }
  else
  {
    for(i=0;i<2000;i++)
    {
      for(j=0;j<2000;j++)
      {
        if(pDis(i,j,nodesX[c3],nodesY[c3])<h3*h3*d2*d2 && 
          Math.sqrt(pDis(i,j,nodesX[c1],nodesY[c1]))+Math.sqrt(pDis(i,j,nodesX[c2],nodesY[c2]))<-2*ah*d1 && 
          Math.sqrt(pDis(i,j,nodesX[c1],nodesY[c1]))+Math.sqrt(pDis(i,j,nodesX[c2],nodesY[c2]))>2*(-ah-1)*d1 )
          {
              ccc+=1;
              if(i%4==0&&j%4==0) {
		            ctx2.fillStyle = "#FF0000";
		            ctx2.fillRect(i,j,2,2);
		          }
	        }
	      
      }
    }
  }
  
  console.log(ccc);
}

//when show all area button is pressed
function showArea() {
    var ds=information[currTextFieldPos].toString().split(";");
    if(ds.length == 5)
    {
      drawCycle2(information[currTextFieldPos]);
    }
    if(ds.length == 7)
    {
      drawHyper2(information[currTextFieldPos]);
    }
    document.getElementById("searchingWSNsModal").style.display = "none";
    setTimeout(function(){
      document.getElementById("searchingWSNsModal").style.display = "block";
    },2000);
}

//when erase button is pressed
function eraseCovered() {
    erase2();
}

//when unkownTwo button is pressed
function routingSim() {
    document.getElementById("searchingWSNsModal").style.display = "none"; 
    disableDrawing();
    disableHopInfo();   
    selectSource = true;
}

function requestRoutingSim(e) {

//obtain current x and y positions of mouse
    currX = e.clientX - canvas.getBoundingClientRect().left;
    currY = e.clientY - canvas.getBoundingClientRect().top;
    selectSource = false;
    var source=-1;
	  for(var i = 0; i < nodesX.length; i++) {
		  //check to see if current mouse x position is in nodesX array
		  if(euDis(currX,currY, nodesX[i],nodesY[i])< 9){
			  //check to see if current Y position is in nodesY array
			  source = i;
			  break;
	    }
    }
    if(constraints.length == 0){
          alert("Please calculate the routing message first");
          return;
    }
    
    if(source == -1) return;


    document.getElementById("loadingBarModal").style.display="block";
    //progress bar variables
    var loadingBar = document.getElementById("loadingBar");
    var progressBar = document.getElementById("progressBar");
    //timer is 2min, 120,000ms = 2min
    const timer = 120000;
    //reset isResponse
    isResponse = false;
    var loadingBarPercent = 1;
    //temp count
    var count = 0;
    loadingBar.style.display = "block";
    progressBar.style.display = "block";
    
    document.getElementById("loadingBarMessage").innerHTML = "Simulating the routing demo in the remote server, Please wait.";
    //loading = setInterval(updateLoadingBar , 100);
    var st="-1";
    if(curInd!=-1)
    {
      st=requestList[curInd].toString();
    }
    
    console.log("request simulating for routing ID: "+st+' &source='+source);
    loadingBar.style.width = 0 + '%';
    
    var call =function(){
        //console.log("reach call");

        
        var u;
        $.ajax({
            url: 'runTOSSIM?resultID='+myID.toString()+st+'&sourceNode='+source,
            type: 'get',
            timeout: 2000,
            error: function(x, textStatus, m) {
                //console.log("reach error: "+textStatus);
                
                if (textStatus=="timeout") {
                   if(loadingBarPercent >= 100)
                   {
                     document.getElementById("loadingBarMessage").innerHTML = "Unable to receive response from server. Please try again";
                   }
                   else
                   {
                     call();
                   }
                   loadingBarPercent = loadingBarPercent + 0.5;
                   loadingBar.style.width = loadingBarPercent + '%';
                }
            },
            success:function(data) {
              loadingBar.style.width = 100 + '%';
              document.getElementById("loadingBarMessage").innerHTML = "Simulation finished. Please close window";
              
              setTimeout(function(){
                  closeLoadingBar();
              }, 1000);
              
            }
        });
    };
    
    call();
}



function iniCanvas3(){
  var canvas3 = document.getElementById("canvas3");
  //canvas is 2d
  var ctx3 = canvas3.getContext("2d");
  ctx3.lineWidth=1;
  for(var i = 0; i < jsonNodes.total; i++){

    ctx3.beginPath();
    ctx3.arc(nodesX[i], nodesY[i], 4, 0, 2 * Math.PI);
    ctx3.stroke(); 
    
  }

}




//when unkownThree button is pressed
function visSim() {
    var st="-1";
    if(curInd!=-1)
    {
      st=requestList[curInd].toString();
    }
    
    if ( !visualSim){
      hideCanvas(); 
      erase3();
      var canvas3 = document.getElementById("canvas3");
      var ctx3 = canvas3.getContext('2d');
      canvas.style.display = "block";
      canvas3.style.display = "block";
      iniCanvas3();
      $.ajax({
          type: 'get',
          url: 'Demo?resultID='+myID.toString()+st,
          success:function(data) {
            
            console.log("return Data "+data.toString());
            var iterations = data.toString().split(";");
            for(var j =0; j < iterations.length; j++){
              var iter = iterations[j].split(" ");
                   
                for (var k = 0; k < iter.length; k++){
                  var rnode = iter[k].split(":");
                  if(rnode.length == 1 && rnode[0]!=undefined){
                    ctx3.beginPath();
                    ctx3.arc(nodesX[parseInt(rnode[0])], nodesY[parseInt(rnode[0])], 4, 0, 2 * Math.PI);
                    ctx3.stroke(); 
                    ctx3.fillStyle = "green";
                    ctx3.fill();
                  
                  }else if(rnode.length == 2 && rnode[0]!=undefined){
                    ctx3.beginPath();
                    ctx3.arc(nodesX[parseInt(rnode[1])], nodesY[parseInt(rnode[1])], 4, 0, 2 * Math.PI);
                    ctx3.stroke(); 
                    ctx3.fillStyle = "red";
                    ctx3.fill();                  
                  }
                }    
                 
            }
            
          }
      });
      
      document.getElementById("searchingWSNsModal").style.display = "none";
    }
    else{
      showCanvas();
      document.getElementById("canvas3").style.display = "none";
    }
    visualSim = !visualSim;
}

//when unkownFour button is pressed
function resetSim() {
    var st="-1";
    if(curInd!=-1)
    {
      st=requestList[curInd].toString();
    }
    if(st == -1) return;
    $.ajax({
          type: 'get',
          url: 'resetSim?resultID='+myID.toString()+st,
          
      });
}

//opens search nodes modal and allows user to input node # to search for node
function searchNodesPopup() {
	//opens search node modal
	document.getElementById("searchNodesModal").style.display = "block";
	
	//gets max number of nodes displayed from array
	var maxNodes = nodesX.length - 1;
	//message to be displayed inside modal
	var message = "";
	
	//if maxNodes is 0 then that means there are no nodes displayed
	if(maxNodes <= 0) {
		message = "No nodes displayed";
		document.getElementById("nodeNumber").disabled = true;
		document.getElementById("searchButton").disabled = true;
	}
	//else there are nodes displayed
	else {
		message = "Please enter a number between 0 and " + maxNodes;
		document.getElementById("nodeNumber").disabled = false;
		document.getElementById("searchButton").disabled = false;
	}
	
	//update the displayed message
	document.getElementById("messageBox").innerHTML = message;
	
	//set focus onto textbox
	document.getElementById("nodeNumber").focus();
}

//takes inputed number from search nodes modal to display node info
function searchNodes() {
	//get value from textbox
	var input = document.getElementById("nodeNumber").value;
	//get max # of nodes
	var maxNodes = nodesX.length - 1;
	//if input is less than 0 or greater than maxNodes-1 then it is out of bounds
	if(input < 0 || input > maxNodes) {
		document.getElementById("errorMessageBox").innerHTML = "Invalid range";
	}
	else {
		//close search nodes modal
		closeSearchNodes();
		nodesX[input];
		nodesY[input];

		//open popup and set its position`
    var popupBox = document.getElementById("popup");
    popupBox.style.display = "block";
    if(anchorNodes[input]==1){popupBox.style.backgroundColor="red";}
    else{
      popupBox.style.backgroundColor="silver";
    }
    
    popupBox.style.top = nodesY[input];
    popupBox.style.left = nodesX[input];
    popupBox.innerHTML = "Node #: " + input + "<br />" + "X: " + nodesX[input] + "<br />" + "Y: " + nodesY[input];
	}
}


function helpPage(){
  $.ajax({
    url: 'helpFile',
    type: 'get',
    contentType: 'application/pdf',
    dataType: 'pdf',
});

}


















