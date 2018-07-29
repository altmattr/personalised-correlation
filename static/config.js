//Config Data:

//Color of nodes, index as rating
var severityChart = 
[
	"rgb(183, 232, 255, 1)",
	"rgb(98, 181, 219, 1)",
	"rgb(29, 134, 183, 1)",
	"rgb(8, 61, 135, 1)",
]

//The modifier to determine the size of a node based off the
//group average
var nodeSizeModifier = 1;
//The maxmimum and minimum size a node can be
var maxNodeSize = 10;
var minNodeSize = 0.5;
//Beta determines the size of a text node.
var nodeTextSize = 8;

//Determines what links will not be displayed 
//i.e anything less than linkMinThresh and anything greater than 
//    linkMaxThreshold
var linkMaxThresh = 10;
var linkMinThresh = 0;
//The default value the correlation strength will display.
var linkThreshold = 5;

//
var linkWidthModifier = 0.5;
//Maximum and Minimum of width/size of all links
var maxLinkWidth = 8;
var minLinkWidth = 0.1;

//The colour of the positive correlations
var posCorrLinkColor = "green";
//The colour of the negative correlations
var negCorrLinkColor = "red";

//Determine if a node is being selected, if true the current selected node will
//Highlight all the links connected to it and remove all other links
var nodeSelect = false;
//The opacity of all links by default.
//I.E. 0 is completely transparent and 1 is opaque.
var linkOpacity = 0.2;
//The opacity of the highlighted link (if a node is being selected)
var linkHOpacity = 1;
var currentOpacity = linkOpacity;

var responsiveWidth = window.innerWidth * 0.7;
//Determines the number of tris
//I.E. Increase the number to improve the image quality of the node.
//     Decrease it to reduce the quality and improve speed
var nodeResolution = 20;
var labelTextColor = "black";
var backgroundColor = "white";

var freqMod = ["Arithmetic Average", "Standard Deviation", "Distributed Average"];
//End of Config 