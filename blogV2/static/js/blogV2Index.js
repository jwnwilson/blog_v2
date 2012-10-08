$(document).ready(function() {
	// Load intro data into blog
	//loadXMLDoc("/data/blog_introText.txt","blog_intro");
});


function loadXMLDoc(filePath, elementID)
{
	var xmlhttp;
	if (window.XMLHttpRequest)
	{// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp=new XMLHttpRequest();
	}
	else
	{
		// code for IE6, IE5
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			document.getElementById(elementID).innerHTML=xmlhttp.responseText;
		}
	}
	xmlhttp.open("GET",filePath,true);
	alert(xmlhttp.responseText);
	xmlhttp.send();
}

