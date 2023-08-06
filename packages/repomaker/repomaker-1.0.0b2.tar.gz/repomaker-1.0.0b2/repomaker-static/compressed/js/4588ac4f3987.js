;var buttonAdd=document.getElementById('rm-app-card-footer-action')
var appsToAdd=[]
var sessionStorageKeyApps='rmAppsToAdd'
var sessionStorageKeyRepo='rmRepo'
var sessionStorageKeyReferrer='rmReferrer'
window.repoId='0'
if(typeof(Storage)!=="undefined"){var sessionStorageAppsToAdd=JSON.parse(sessionStorage.getItem(sessionStorageKeyApps))
if(sessionStorageAppsToAdd!==null&&sessionStorageAppsToAdd.length!==0&&appsToAdd.length===0){appsToAdd=sessionStorageAppsToAdd
markAppsToAdd()
updateAppsToAddCount()}
var sessionStorageRepo=JSON.parse(sessionStorage.getItem(sessionStorageKeyRepo))
if(sessionStorageRepo!==null&&sessionStorageRepo.length!==0&&window.repoId===0){window.repoId=sessionStorageRepo}}
function addRemoteApp(event,repoId,appRepoId,appId,remoteAddUrl){event.preventDefault()
event.stopPropagation()
if(window.repoId==='0'){window.repoId=repoId
sessionStorage.setItem(sessionStorageKeyRepo,repoId)}
else if(window.repoId!==repoId){throw new Error('Repository ID where the apps should be added to differs')}
var app={appRepoId:appRepoId,appId:appId}
var element='rm-app-card-footer-action--'+appId
var appAlreadyAdded=false
for(var i=0;i<appsToAdd.length;i++){if(appsToAdd[i].appRepoId==appRepoId&&appsToAdd[i].appId==appId){appAlreadyAdded=true
if(!remoteAddUrl){appsToAdd.splice(i,1)}
buttonSetNormal(element)
break}}
if(!appAlreadyAdded){appsToAdd.push(app)
buttonSetAdded(element)}
if(typeof(Storage)!=="undefined"){sessionStorage.setItem(sessionStorageKeyApps,JSON.stringify(appsToAdd))
updateAppsToAddCount()}
if(remoteAddUrl){location.href=remoteAddUrl}}
function back(event){if(appsToAdd.length===0){return}
if(window.repoId==='0'){window.repoId=sessionStorage.getItem(sessionStorageKeyRepo)}
event.preventDefault()
var url=Urls.add_app(window.repoId)
var request=new XMLHttpRequest()
request.onreadystatechange=function(){if(request.readyState===4){appsAdded(request)}}
request.open("POST",url,true)
request.setRequestHeader("X-CSRFToken",document.getElementsByName('csrfmiddlewaretoken')[0].value)
request.setRequestHeader('X-REQUESTED-WITH','XMLHttpRequest')
request.send(JSON.stringify(appsToAdd))}
function appsAdded(request){if(request.status===204){if(typeof(Storage)!=="undefined"){sessionStorage.removeItem(sessionStorageKeyApps)
sessionStorage.removeItem(sessionStorageKeyRepo)}
window.location=Urls.repo(window.repoId)}
else{showError(request.responseText)}}
function markAppsToAdd(){for(var i=0;i<appsToAdd.length;i++){var element='rm-app-card-footer-action--'+appsToAdd[i]['appId']
buttonSetAdded(element)}}
function updateAppsToAddCount(){var count=appsToAdd.length
var countContainer=document.querySelector('.rm-repo-add-toolbar-count')
if(countContainer===null){return}
countContainer.hidden=false
var countText=document.getElementById('rm-repo-add-toolbar-count-text')
if(count>0){countText.textContent=interpolate(ngettext('%s app added','%s apps added',count),[count])}
else{countContainer.hidden=true}}
function clearAppsToAdd(event){if(typeof(Storage)!=="undefined"){sessionStorage.removeItem(sessionStorageKeyApps)}}
function buttonSetAdded(element){addClassToElement(element,'rm-app-card-footer-action--successful')
setContentOfElement(element+'-button','<i class="material-icons">done</i>')}
function buttonSetNormal(element){setClassOfElement(element,'rm-app-card-footer-action')
setContentOfElement(element+'-button',gettext('Add'))}
function showError(text){var element='rm-app-add-errors'
setContentOfElement(element,text)
setHiddenOfElement(element,false)}
function setClassOfElement(element,myClass){element=document.getElementById(element)
if(element!==null){element.className=myClass}}
function addClassToElement(element,myClass){element=document.getElementById(element)
if(element!==null){element.classList.add(myClass)}}
function removeClassFromElement(element,myClass){element=document.getElementById(element)
if(element!==null){element.classList.remove(myClass)}}
function setContentOfElement(element,content){element=document.getElementById(element)
if(element!==null){element.innerHTML=content}}
function setHiddenOfElement(element,hidden){if(typeof element==='string'){element=document.getElementById(element)}
if(element!==null){element.hidden=hidden}}
var mdlBody=document.querySelector('.mdl-layout__content')
var pagination=document.querySelector('.rm-pagination')
mdlBody.addEventListener("scroll",function(){if(mdlBody.scrollHeight-window.innerHeight-
mdlBody.scrollTop<=800){if(pagination!==null){handlePagination(jsonHtmlRelation,'.rm-app-add-apps',markAppsToAdd)}}},false)
window.onload=function(){if(pagination!==null&&isVisible(pagination)){handlePagination(jsonHtmlRelation,'.rm-app-add-apps',markAppsToAdd)}}
var jsonHtmlRelation={'rm-app-card-categories':'categories','rm-app-card-description':'description','rm-app-card-footer-action':'id','rm-app-card-left':'icon','rm-app-card-summary':'summary','rm-app-card-title':'name','rm-app-card-updated':'updated','rm-app-card--apps-add':'id',}
var searchInput=document.querySelector('.rm-app-add-filters-search-input')
var searchClear=document.querySelector('.rm-app-add-filters-search-clear')
if(searchInput!==null){setHiddenOfElement(searchClear,(searchInput.value.length===0))
searchInput.addEventListener("input",function(){setHiddenOfElement(searchClear,(searchInput.value.length===0))})}