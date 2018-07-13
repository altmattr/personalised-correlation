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

var responsiveWidth = window.innerWidth * 0.7;
var nodeResolution = 20;
var labelTextColor = "black";
var backgroundColor = "white";

var freqMod = ["Arithmetic Average", "Standard Deviation", "Distributed Average"];
//End of Config 