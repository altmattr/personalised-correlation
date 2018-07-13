//Config Data:

//Variables i need from Oscar

//Color of nodes, index as rating
var severityChart = 
[
	"rgb(183, 232, 255, 1)",
	"rgb(98, 181, 219, 1)",
	"rgb(29, 134, 183, 1)",
	"rgb(8, 61, 135, 1)",
]

var nodeSizeModifier = 0.1;
var maxNodeSize = 10;
var minNodeSize = 0.5;
var nodeTextSize = 8;

//Determines what links will be displayed 
//i.e anything less than -linkThreshold and anything greater than linkThreshold
var linkMaxThresh = 10;
var linkMinThresh = 0;
var linkThreshold = 5;
var linkWidthModifier = 0.5;
var maxLinkWidth = 8;
var minLinkWidth = 0.1;
var posCorrLinkColor = "green";
var negCorrLinkColor = "red";

//Determine if a node is being selected, if true the current selected node will
//Highlight all the links connected to it and remove all other links
var nodeSelect = false;
var linkOpacity = 0.2;
var linkHOpacity = 1;
var currentOpacity = linkOpacity;

var nodeResolution = 20;
var labelTextColor = "black";
var backgroundColor = "white";
//End of Config 

//----
//Other variables:
var linkIdxStatus = 0;
var linkMode = ["Only Positive", "Only Negative", "All"]

let toggledNode = "";
let gData = [];

//Button functionality:
function alterLinks() {
	if (linkIdxStatus < linkMode.length-1)
		linkIdxStatus++;
	else
		linkIdxStatus = 0;
	document.getElementById("alterLinks").innerHTML = linkMode[linkIdxStatus];
	create3DGraph();
}


// Node
function createNodes(dataMatrix, symptomRatings){
	var nodes = [];
	for (var i = 1; i < dataMatrix.length; i++){
		symptIdx = i-1;
		var colorIdx = symptomRatings[symptIdx][2]-1;
		var nodeRadius = symptomRatings[symptIdx][1];
		nodeRadius *= nodeSizeModifier;
		nodeRadius = Math.max(Math.min(nodeRadius, maxNodeSize), minNodeSize);
		//Node in the form: 
		//nodes.push({id:node ID make sure this is the same as linked, index: idx or id of node by unique number 0 - (max node-1), color: colour of node, 
		//radius: size of node, symptom: name of symptom)
		nodes.push({id:dataMatrix[0][i], index: i, color:severityChart[colorIdx], radius:nodeRadius, symptom:symptomRatings[symptIdx][0]});
	}
	return nodes;
}



function createLinks(dataMatrix){
	var links = [];
	for (var i = 1; i < dataMatrix.length; i++){
		for (var j = i+1; j < dataMatrix.length; j++){
			let corrData = +dataMatrix[i][j];
			//Links in the form: 
			//source: which node to link from, target: which node to link to,
			//width: size of link, color: colour of link, isReverse: true if is negative correlation else false}}
			let source = dataMatrix[i][0];
			//Sets the values if the a node is currently being selected 
			if (nodeSelect == true){
				if (toggledNode !== source)
					continue
			}
			//Setting link data
			if (corrData > linkThreshold && linkIdxStatus != 2){
				corrData *= linkWidthModifier;
				corrData = Math.max(Math.min(corrData, maxLinkWidth), minLinkWidth);
				links.push({source: source, target: dataMatrix[0][j], width: corrData, color: posCorrLinkColor, isReverse: false});
			}
			else if (corrData < -linkThreshold && linkIdxStatus != 1){
				corrData *= linkWidthModifier;
				corrData *= -1;
				corrData = Math.max(Math.min(corrData, maxLinkWidth), minLinkWidth);
				links.push({source: source, target: dataMatrix[0][j], width: corrData-1, color: negCorrLinkColor, isReverse: true});
			}
		}
	}
	return links;
}

function create3DGraph(worded){
	//Calls Create Node to generate array of node objects.
	let nodes = createNodes(dataMatrix, symptomRatings);
	//Calls CreateLinks to generate array of Link objects.
	let dataLinks = createLinks(dataMatrix);
	gData = {
		nodes: nodes,
		links: dataLinks,
	}
	if (worded == true)
		generateWord3DGraph();
	else	
		generate3DGraph();
	
}

function checkThreshold(){
	linkThreshold = document.getElementById("corrStrText").value;
	linkThreshold = Math.max(Math.min(linkThreshold, linkMaxThresh), linkMinThresh);
	document.getElementById("corrStrText").value = linkThreshold;
}

function generate3DGraphButton(worded){
	checkThreshold();
	create3DGraph(worded);
}

function generateWord3DGraph(){
	let elem = document.getElementById('3d-graph');
	
	let Graph = ForceGraph3D();
	Graph(elem)
		.nodeColor('color')
		.nodeVal('radius')
		.linkWidth('width')
		.linkColor('color')
		.backgroundColor(backgroundColor)
		//Resolution 20 looks good, 0 looks like rectangles
		.nodeResolution(nodeResolution)
		//Opacity is set between 0 and 1 where 0 is transparent and 1 is opaque
		.linkOpacity(currentOpacity)
		.nodeOpacity(1)
		.onNodeClick(toggleHighlightNode)
		.nodeThreeObject(node => {
          let txtSprite = new SpriteText(node.id);
          txtSprite.color = node.color;
          txtSprite.textHeight = nodeTextSize;
          return txtSprite;
		})
		.graphData(gData);
}

function generate3DGraph(){
	let elem = document.getElementById('3d-graph');
	
	let Graph = ForceGraph3D();
	Graph(elem)
		.nodeColor('color')
		.nodeVal('radius')
		.linkWidth('width')
		.linkColor('color')
		.backgroundColor(backgroundColor)
		//Resolution 20 looks good, 0 looks like rectangles
		.nodeResolution(nodeResolution)
		//Opacity is set between 0 and 1 where 0 is transparent and 1 is opaque
		.linkOpacity(currentOpacity)
		.nodeOpacity(1)
		.onNodeClick(toggleHighlightNode)
		//Displays the text when hovering a node.
		.nodeLabel(function(node){
			var label = "<p style="+'"'+"color:"+ labelTextColor +'"'+">" + node.symptom + "</p>";
			return label;
		})
		.graphData(gData);
}

function toggleHighlightNode(node){
	currentOpacity = linkOpacity;
	if (nodeSelect == false){
		toggledNode = node.id;
		currentOpacity = linkHOpacity;
	}
	nodeSelect = !nodeSelect;
	create3DGraph();
}