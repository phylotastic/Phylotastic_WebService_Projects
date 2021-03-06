/*  it requires jquery loaded */
var ete_webplugin_URL = "http://localhost:3031";//"http://localhost:8990";
var loading_img = '<img border=0 src="loader.gif">';

//var ete_webplugin_URL = "http://phylo.cs.nmsu.edu:8990";
//var loading_img = '<img border=0 src="http://phylo.cs.nmsu.edu:8080/TreeViewer/demo/loader.gif">';

var current_tree_id = "";
var current_tree_newick = "";
var node_actions_list = [];
var tree_actions = {};
var latest_action_node_id = ""

function update_server_status(){
  console.log('updating');
  $('#server_status').load(ete_webplugin_URL+"/status");

}
//------------------------------------------
function save_tree_image(){
  $('#svg_image').html(loading_img);
  format = $('input[name="format"]:checked').val();

  xhr = new XMLHttpRequest();
  var url = ete_webplugin_URL+'/save_tree_image';
  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-type", "application/json");
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
        var hres = JSON.parse(xhr.responseText);
        $('#svg_image').html(hres.html_data);
    }
  }
  //parameters for POST request 
  var params = JSON.stringify({"tree_newick": current_tree_newick,"tree_id":current_tree_id, "actions":{"tree_actions": tree_actions, "node_actions": node_actions_list, "latest_action_node_id":latest_action_node_id},"format": format});
  xhr.send(params); 
}

//----------------------------------------------------
function get_tree_image(treeid, newick, recipient){
  current_tree_id = treeid;
  current_tree_newick = newick;
  //console.log("recipient:" + recipient);
  
  if (recipient != ''){
     $(recipient).html('<div id="' + treeid + '">' + loading_img + '</div>');
     node_actions_list = [];
     tree_actions = {};
     latest_action_node_id = "";
     $('#message').html("");
  }
  xhr = new XMLHttpRequest();
  var url = ete_webplugin_URL+'/get_tree_image';
  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-type", "application/json");
  xhr.onreadystatechange = function () { 
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("got response");
        console.log(typeof(xhr.responseText));
        //var jsonStr = JXG.decompress(xhr.responseText);
        //console.log("type jsonStr:"+typeof(jsonStr));
        //var hres = JSON.parse(jsonStr); 
        //console.log(hres);
        var hres = JSON.parse(xhr.responseText);
        //update the global tree actions
        var ta = hres.actions["tree_actions"];
        if (typeof(ta) != "undefined"){ 
           tree_actions = ta;
           //console.log("ta:"+JSON.stringify(tree_actions));
        }
        //update the global node actions
        var na = hres.actions["node_actions"];
        if (typeof(na) != "undefined"){
           node_actions_list = na;
           //console.log("na:"+JSON.stringify(node_actions_list));
        }
        //console.log("na: "+typeof(na)); 
        $('#'+treeid).html(hres.html_data);
        $('#'+treeid).fadeTo(100, 0.9);
    }
    else if (xhr.status != 200) {
        document.getElementById("message").innerHTML = xhr.responseText;
        $(".ete_image").html("");
        //document.getElementById(treeid).innerHTML = "";
    }
  }
  //console.log("na"+JSON.stringify(node_actions_list));
  //parameters for POST request 
  var params = JSON.stringify({"tree_newick": newick,"tree_id":treeid,"actions":{"tree_actions": tree_actions, "node_actions": node_actions_list, "latest_action_node_id":latest_action_node_id}});
  xhr.send(params);
}
/*
function get_tree_image(treeid, newick, recipient, topOffset, leftOffset){
  topOffset = (typeof topOffset !== 'undefined') ? topOffset : 0;
  leftOffset = (typeof leftOffset !== 'undefined') ? leftOffset : 0;

  current_tree_id = treeid;
  current_tree_newick = newick;
  //console.log("recipient:" + recipient);
  if (recipient != ''){
     $(recipient).html('<div id="' + treeid + '">' + loading_img + '</div>');
     node_actions_list = [];
     tree_actions = {};
     latest_action_node_id = "";
  }
  xhr = new XMLHttpRequest();
  var url = ete_webplugin_URL+'/get_tree_image';
  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-type", "application/json");
  xhr.onreadystatechange = function () { 
    if (xhr.readyState == 4 && xhr.status == 200) {
        var hres = JSON.parse(xhr.responseText);
        //update the global tree actions
        var ta = hres.actions["tree_actions"];
        if (typeof(ta) != "undefined"){ 
           tree_actions = ta;
           //console.log("ta:"+JSON.stringify(tree_actions));
        }
        //update the global node actions
        var na = hres.actions["node_actions"];
        if (typeof(na) != "undefined"){
           node_actions_list = na;
           //console.log("na:"+JSON.stringify(node_actions_list));
        }
        //console.log("na: "+typeof(na)); 
        $('#'+treeid).html(hres.html_data);
        $('#'+treeid).fadeTo(100, 0.9);
    }
  }
  //parameters for POST request 
  var params = JSON.stringify({"tree_newick": newick,"tree_id":treeid, 'top_offset': topOffset, 'left_offset': leftOffset, "actions":{"tree_actions": tree_actions, "node_actions": node_actions_list, "latest_action_node_id":latest_action_node_id}});
  xhr.send(params);
}*/

//-----------------------------------------
function show_actions(treeid, nodeid){
  $("#popup").html(loading_img);
  xhr = new XMLHttpRequest();
  var url = ete_webplugin_URL+'/get_actions';
  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-type", "application/json");
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
        var hres = JSON.parse(xhr.responseText);
        //console.log("html_data: "+hres.html_data);
        $('#popup').html(hres.html_data);
    }
  }
  //parameters for POST request 
  var params = JSON.stringify({"tree_newick": current_tree_newick,"tree_id":current_tree_id,"node_actions": node_actions_list, "node_id":nodeid});
  xhr.send(params);
  
}
//------------Node Action---------------------------
function run_action(treeid, nodeid, aindex){
  $("#popup").hide();
  $('#'+treeid).html(loading_img);
  //console.log(treeid, nodeid, faceid, aindex, $('#'+treeid));
  latest_action_node_id = nodeid;
  //console.log("nodeid type:"+typeof(nodeid));
  update_node_action(nodeid, aindex);
  //console.log("runaction called..na:"+JSON.stringify(node_actions_list));
  get_tree_image(current_tree_id, current_tree_newick,'');
}

//----------------------------------------
function update_node_action(nodeid, aindex){
  //console.log("update node action called");
  var len = node_actions_list.length;
  var node_found = false;
  aindex = aindex.toLowerCase();
  //console.log("aindex: "+aindex+" nodeid: "+nodeid);
  alter_actions = ["expand"]
  for (i=0; i < len; i++){
     node_action_obj = node_actions_list[i];
     node_id = node_action_obj["node_id"];
     //update action of an existing node
     if (node_id == nodeid){
        node_found = true;
        if (aindex in node_action_obj){
           action_val = node_action_obj[aindex];
           node_action_obj[aindex] = !action_val;
        } 
        else{
           ain = alter_actions.indexOf(aindex);
           //if (ain != -1 && aindex == alter_actions[0]){
           //   node_action_obj["display_picture"] = false;
           //}
           if(ain != -1 && aindex == alter_actions[0]){
              node_action_obj["collapse"] = false;
           }
           else{
              node_action_obj[aindex] = true;
           }
        }
     }
  }//end of for
  //add action of a new node
  if (!node_found){
    node_action = {};
    node_action["node_id"] = nodeid;

    ain = alter_actions.indexOf(aindex);
    //if (ain != -1 && aindex == alter_actions[0]){
    //   node_action["display_picture"] = false;
    //}
    if(ain != -1 && aindex == alter_actions[0]){
       node_action["collapse"] = false;
    }
    else
       node_action[aindex] = true;
    node_actions_list.push(node_action);
  }
  //console.log(JSON.stringify(node_actions_list));
}
//-------------TreeAction------------------------
function run_tree_action() {
    colorcode = document.getElementsByName("color")[0].value;
    linewidth = $('input[name="lwidth"]:checked').val();
    /*if(document.getElementById('ladderize').checked){
        ladderize = true;
    }else{
        ladderize = false;
    }*/
    ladderize = $("#ladderize").is(':checked');
    console.log("ladderize:"+ladderize);
    showbranch = $("#branch").is(':checked');
    showinternal = $("#internal").is(':checked');
    $('#'+current_tree_id).html(loading_img);

    tree_actions = {"line_color":colorcode,"line_width": linewidth ,"ladderize": ladderize, "show_branch_length": showbranch, "show_internal_node": showinternal};
    //console.log(JSON.stringify(tree_actions));
    get_tree_image(current_tree_id, current_tree_newick,'');
}
//-------------------------------------------
function load_tip_images(){
  var service_url = "http://localhost:5008/phylotastic_ws/ds/";
  var service_func1 = "images_download_time";
  //var service_url = "http://phylo.cs.nmsu.edu:5008/phylotastic_ws/ds/images_download_time";
  var service_param = "newick="+ encodeURIComponent(current_tree_newick);
  //var service_param = {"newick": current_tree_newick};  

  xhr = new XMLHttpRequest();
  xhr.open("POST", service_url+service_func1, true);
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
        var hres = JSON.parse(xhr.responseText);
        if (hres.number_species != 0){
           $('#message').html("Approximate time for Downloading all images is "+hres.download_time+"s. Please wait until notified of completion of download");
           var pm = {"newick":current_tree_newick}
           $('#message').load(service_url+"/download_all_images", pm);
        }
        else{
           xhr2 = new XMLHttpRequest();
           var url2 = ete_webplugin_URL+'/set_all_images';
           xhr2.open("POST", url2, true);
           xhr2.setRequestHeader("Content-type", "application/json");
           xhr2.onreadystatechange = function () {
              if (xhr2.readyState == 4 && xhr2.status == 200) {
                 var hres2 = JSON.parse(xhr2.responseText);
                 var ndac = hres2.actions["node_actions"];
                 //console.log("na load:"+JSON.stringify(ndac));
                 if (typeof(ndac) != "undefined"){
                    node_actions_list = ndac;
                    //console.log("na in load:"+JSON.stringify(node_actions_list));
                 }
                 $('#message').html("Please wait while the tree is drawn.");
                 $("#img1").html('<div id="' + current_tree_id + '">' + loading_img + '</div>');
                 get_tree_image(current_tree_id, current_tree_newick,'');
              }
           }
           //parameters for second POST request 
           var params2 = JSON.stringify({"tree_newick": current_tree_newick,"tree_id":current_tree_id, "node_actions": node_actions_list});
           xhr2.send(params2);
        }//end of else
     }
  }//end of xhr
  //parameters for POST request 
  xhr.send(service_param);
}
//----------------------------------------------
function set_all_picture(){
  console.log("set all picture called");
  var len = node_actions_list.length;
  var node_found = false;
  
  for (i=0; i < len; i++){
     node_action_obj = node_actions_list[i];
     node_id = node_action_obj["node_id"];
     //update action of an existing node
     if (node_id == nodeid){
        node_found = true;
        if (aindex in node_action_obj){
           action_val = node_action_obj[aindex];
           node_action_obj[aindex] = !action_val;
        }
        else{
           ain = alter_actions.indexOf(aindex);
           //if (ain != -1 && aindex == alter_actions[0]){
           //   node_action_obj["display_picture"] = false;
           //}
           if(ain != -1 && aindex == alter_actions[0]){
              node_action_obj["collapse"] = false;
           }
           else{
              node_action_obj[aindex] = true;
           }
        }
     }
  }//end of for
  //add action of a new node
  if (!node_found){
    node_action = {};
    node_action["node_id"] = nodeid;

    ain = alter_actions.indexOf(aindex);
    if (ain != -1 && aindex == alter_actions[0]){
       node_action["display_picture"] = false;
    }
    else if(ain != -1 && aindex == alter_actions[1]){
       node_action["collapse"] = false;
    }
    else
       node_action[aindex] = true;
  }
}

//-------------------------------------------
function bind_popup(){
  $(".ete_tree_img").bind('click',function(e){
      $("#popup").css('left', e.pageX - 2);
      $("#popup").css('top', e.pageY - 2);
      $("#popup").css('position',"absolute" );
      $("#popup").css('background-color',"#fff" );
      $("#popup").draggable({ cancel: 'span,li' });
      $("#popup").show();
   });
   
}

/*function bind_popup(leftOffset, topOffset){
  topOffset = (typeof topOffset !== 'undefined') ? topOffset : 0;
  leftOffset = (typeof leftOffset !== 'undefined') ? leftOffset : 0;
  $(".ete_tree_img").bind('click',function(e){
      $("#popup").css('left', e.pageX - leftOffset);
      $("#popup").css('top', e.pageY - topOffset);
      $("#popup").css('position',"absolute" );
      $("#popup").css('background-color',"#fff" );
      $("#popup").draggable({ cancel: 'span,li' });
      $("#popup").show();
      e.preventDefault();
      return false;
   });
   $(".ete_tree_img").bind('click', function(e) {
     $("#popup").css("display", "none");
   })

   $(".ete_tree_img + div").bind('click', function(e) {
     $('#popup').css('display', 'none');
   })

}*/

function hide_popup(){
  $('#popup').hide();
}

//-------------OTHERS----------------------

function highlight_node(treeid, nodeid, faceid, x, y, width, height){
  return;
  console.log(treeid, nodeid, x, y, width, height);
  var img = $('#img_'+treeid);
  var offset = img.offset();
  console.log(img);
  console.log(offset);

  $("#highlighter").show();
  $("#highlighter").css("top", offset.top+y-1);
  $("#highlighter").css("left", offset.left+x-1);
  $("#highlighter").css("width", width+1);
  $("#highlighter").css("height", height+1);

}
function unhighlight_node(){
  return;
  console.log("unhighlight");
  $("#highlighter").hide();
}

function makeid()
{
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < 5; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}


///////OLD STUFF


$(document).ready(function(){
  hide_popup();
});
