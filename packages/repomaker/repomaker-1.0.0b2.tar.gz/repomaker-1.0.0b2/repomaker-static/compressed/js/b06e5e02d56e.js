;var rmPaginationPage=null
var DIV_REPO_ID='rm-repo-id'
function handlePagination(jsonHtmlRelation,appList,loadingFinished){var pagination=document.querySelector('.rm-pagination')
if(pagination.hidden||rmPaginationPage===0){return}
var paginationLoading=document.querySelector('.rm-pagination--loading')
pagination.hidden=true
paginationLoading.hidden=false
var urlString=window.location.href
var url=new URL(urlString)
if(rmPaginationPage===null){rmPaginationPage=2
pageParam=url.searchParams.get('page')
if(pageParam!==null&&pageParam.length!==0){rmPaginationPage=parseInt(pageParam)+1}}
searchParam=url.searchParams.get('search')
if(searchParam===null||searchParam.length===0){urlString=urlString.split('?')[0]+'?page='+rmPaginationPage}
else{urlString=urlString.split('?')[0]+'?search='+searchParam+'&page='+rmPaginationPage}
var request=new XMLHttpRequest()
request.onreadystatechange=function(){if(request.readyState===4){if(request.status!==404){appendApps(jsonHtmlRelation,appList,request)
pagination.hidden=false
paginationLoading.hidden=true
rmPaginationPage=rmPaginationPage+1
if(loadingFinished!==undefined){loadingFinished()}
if(isVisible(pagination)){handlePagination(jsonHtmlRelation,appList)}}
else{rmPaginationPage=0
paginationLoading.hidden=true}}}
request.open("GET",new URL(urlString),true)
request.setRequestHeader('X-REQUESTED-WITH','XMLHttpRequest')
request.send()}
function appendApps(jsonHtmlRelation,appList,request){var apps=JSON.parse(request.response)
var appList=document.querySelector(appList)
var appCardTemplate=document.querySelector('.rm-app-card')
for(app in apps){var newAppCard=appCardTemplate.cloneNode(true)
newAppCard=putAppInformation(jsonHtmlRelation,apps[app],newAppCard)
appList.appendChild(newAppCard)}}
function putAppInformation(jsonHtmlRelation,app,appCard){for(rel in jsonHtmlRelation){if(rel==='rm-app-card-left'){var icon=app[jsonHtmlRelation[rel]]
appCard.querySelector('.'+rel).style.backgroundImage=''
if(icon!==undefined){appCard.querySelector('.'+rel).style.backgroundImage='url("'+app[jsonHtmlRelation[rel]]+'")'}
continue}
if(rel==='rm-app-card-description'){var description=app[jsonHtmlRelation[rel]].replace(/<(?:.|\n)*?>/gm,'')
if(description.length>=165){appCard.querySelector('.'+rel).innerHTML=description.substring(0,168)+'...'
continue}
appCard.querySelector('.'+rel).innerHTML=description
continue}
if(rel==='rm-app-card-footer-action'){var element=appCard.querySelector('.'+rel)
var parent=element.parentElement
if(element!==null){parent.removeChild(element)}
if(app['added']){element=document.createElement('span')
element.classList.add(rel)
var button=document.createElement('button')
button.disabled=true
button.innerText=gettext('Added')
element.appendChild(button)
parent.appendChild(element)
continue}
element=document.createElement('a')
element.classList.add(rel)
var appId=app[jsonHtmlRelation[rel]]
var repoId=document.getElementById(DIV_REPO_ID).dataset.id
var remoteRepoId=app['repo_id']
var lang=app['lang']
element.id=rel+'--'+appId
element.href=Urls.add_remote_app(repoId,remoteRepoId,appId,lang)
element.addEventListener('click',function(event){addRemoteApp(event,parseInt(repoId),remoteRepoId,appId)})
var button=document.createElement('button')
button.id=rel+'--'+appId+'-button'
button.innerText=gettext('Add')
element.appendChild(button)
parent.appendChild(element)
continue}
if(rel==='rm-app-card-categories'){var categories=app[jsonHtmlRelation[rel]]
var categoriesHtml=appCard.querySelector('.'+rel)
while(categoriesHtml.firstChild){categoriesHtml.removeChild(categoriesHtml.firstChild)}
for(var i=0;i<categories.length;i++){var chip=document.createElement('span')
chip.classList.add('rm-app-card-category-chip','mdl-chip')
var chipText=document.createElement('span')
chipText.classList.add('rm-app-card-category-text','mdl-chip__text')
chipText.innerText=categories[i]['name']
chip.appendChild(chipText)
categoriesHtml.appendChild(chip)}
continue}
if(rel==='rm-app-card--repo-apps'){var repoId=document.getElementById(DIV_REPO_ID).dataset.id
var appId=app[jsonHtmlRelation[rel]]
var url=Urls.app(repoId,appId)
appCard.href=url
continue}
if(rel==='rm-app-card--apps-add'){appCard.removeAttribute('onclick')
if(app['added']){appCard.classList.add('rm-app-card--no-hover')
continue}
if(appCard.classList.contains('rm-app-card--no-hover')){appCard.classList.remove('rm-app-card--no-hover')}
var repoId=document.getElementById(DIV_REPO_ID).dataset.id
var remoteRepoId=app['repo_id']
var appId=app[jsonHtmlRelation[rel]]
var lang=app['lang']
var url=Urls.add_remote_app(repoId,remoteRepoId,appId,lang)
appCard.addEventListener('click',function(event){window.location.href=url})
continue}
var element=appCard.querySelector('.'+rel)
if(element===null){element=document.createElement('div')
element.classList.add(rel)}
var content=app[jsonHtmlRelation[rel]]
element.innerHTML=''
if(content!==undefined){element.innerHTML=app[jsonHtmlRelation[rel]]}}
return appCard}
function isVisible(element){var docViewBottom=mdlBody.scrollTop+window.innerHeight
var elementTop=element.offsetTop
return(elementTop<=docViewBottom)}