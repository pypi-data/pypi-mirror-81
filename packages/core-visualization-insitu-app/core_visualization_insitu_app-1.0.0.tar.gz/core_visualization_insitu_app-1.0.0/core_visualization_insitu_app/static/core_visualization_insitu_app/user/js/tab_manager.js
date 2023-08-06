function openBuildCommandTab(evt, tabNumber) {
  var i, buildCommandtabcontent, buildCommandtablinks;
  buildCommandtabcontent = document.getElementsByClassName("buildCommandtabcontent");
  for (i = 0; i < buildCommandtabcontent.length; i++) {
    buildCommandtabcontent[i].style.display = "none";
    buildCommandtabcontent[i].className = buildCommandtabcontent[i].className.replace(" tabContentActive", "");
  }
  buildCommandtablinks = document.getElementsByClassName("buildCommandtablinks");
  for (i = 0; i < buildCommandtablinks.length; i++) {
    buildCommandtablinks[i].className = buildCommandtablinks[i].className.replace(" active", "");
  }
  document.getElementById(tabNumber).style.display = "block";
  evt.currentTarget.className += " active";
  document.getElementById(tabNumber).className += " tabContentActive";
}

function openLayerWiseTab(evt, tabNumber) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("layerWisetabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
    tabcontent[i].className = tabcontent[i].className.replace(" tabContentActive", "");
  }
  tablinks = document.getElementsByClassName("layerWisetablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(tabNumber).style.display = "block";
  evt.currentTarget.className += " active";
  document.getElementById(tabNumber).className += " tabContentActive";

}

function openMeltPoolTab(evt, tabNumber) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("meltPooltabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
    tabcontent[i].className = tabcontent[i].className.replace(" tabContentActive", "");
  }
  tablinks = document.getElementsByClassName("meltPooltablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(tabNumber).style.display = "block";
  evt.currentTarget.className += " active";
  document.getElementById(tabNumber).className += " tabContentActive";
}


// .ready() called.
$(function() {
    document.getElementById("buildCommandDefaultOpen").click();
    document.getElementById("layerWiseDefaultOpen").click();
    document.getElementById("meltPoolDefaultOpen").click();

});