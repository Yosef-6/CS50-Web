

const messageDanger     = 'alert alert-danger'
const messageSuccess    = 'alert alert-success'

const mainDivClassName  = "col-12 mb-3"
const subDivClassName   = "card-body"
const innerDivClassName = "d-flex flex-start align-items-center"
const headerClassName   = "fw-bold text-primary mb-1"
const headerStyle       = "margin-left:11px"
const p1className       = "text-muted small mb-0"
const p2className       = "mt-3 mb-4 pb-2"
const p2style           = "margin-left:80px;word-wrap: break-word;"
let   currentUser       = ''    
const flashMessage      = ["postSaved","statusUpsdate"] // if post is saved fetch post or if its a status update dont fetch
let   flash             = flashMessage[0] // default
document.addEventListener("DOMContentLoaded",()=>{
        currentUser = JSON.parse(document.getElementById('user_name').textContent) 

        document.getElementById("search").addEventListener("keydown",()=>{
                
                setTimeout(()=>{
                         fetch_users("search",document.getElementById("search").value)
                        },1)
                
        })  

        document.getElementById("postTab").addEventListener("click",(e)=>{
                
                target = e.target   
                while(target.getAttribute("data-footer_id") === null && target !== document.getElementById("postTab")){
                        target = target.parentNode
                      } 
                
                 
                if(e.target.tagName === 'BUTTON' || e.target.parentNode.tagName === 'BUTTON'){
                        contentSection = document.querySelector(`div[data-content_id='${target.dataset.footer_id}']`)
                        body = ''
                        document.querySelector(`div[data-content_id='${target.dataset.footer_id}']`).childNodes.forEach((e)=>{if(e.tagName === "P2")body = e.innerHTML})
                        contentSection.innerHTML = ''                   
                        inputField = document.createElement("textarea")  
                        saveButton = document.createElement("button")
                        inputField.className = "form-control"
                        inputField.setAttribute("id","editInput")
                        inputField.setAttribute("data-edit_input_id",`${target.dataset.footer_id}`)
                        inputField.setAttribute("rows","0")
                        inputField.setAttribute("cols","100%")
                        inputField.value = body
                        saveButton.setAttribute("type","submit")
                        saveButton.setAttribute("data-save_id",`${target.dataset.footer_id}`)
                        saveButton.className = "btn btn-primary mt-2"
                        contentSection.append(inputField,saveButton)
                        saveButton.appendChild(document.createTextNode("Save"))
                        document.querySelector(`button[data-save_id='${target.dataset.footer_id}']`).addEventListener("click",(e)=>{

                                e.stopPropagation() // this would be captured by the main div click event so stop the propagation
                                save_post(false,e.target.dataset.save_id)
                                document.querySelector(`textarea[data-edit_input_id='${e.target.dataset.save_id}']`).addEventListener(("animationend"),(e)=>{
                                         
                                        editedContent = e.target.value
                                        p=document.createElement("p")
                                        p.appendChild(document.createTextNode(`${editedContent}`))
                                        e.target.parentNode.appendChild(p)
                                        e.target.parentNode.removeChild(e.target.nextSibling)
                                        e.target.parentNode.removeChild(e.target)
                                            

                                })
                                document.querySelector(`textarea[data-edit_input_id='${e.target.dataset.save_id}']`).setAttribute("id","closeEditInput")

                        })
                }
                else if((e.target.tagName === 'svg'|| e.target.parentNode.tagName === 'svg' )){
               

                        if(currentUser != ''){
                        svg = getElm(e.target,e.target.parentNode,"fill")

                                if(svg.getAttribute("fill") === 'lightgrey'){
                                svg.setAttribute('fill','red'); 
                                like_post(target.dataset.footer_id,true)
                                }
                                else{
                                svg.setAttribute('fill','lightgrey');
                                like_post(target.dataset.footer_id,false)
                                }
                        }
                        else{
                        flash = flashMessage[1]
                        runInfoTab("Login Required",messageDanger);
                        }

            
                }

                
        })
               
        document.getElementById("info").addEventListener("animationend",()=>{
             
             if(flash === flashMessage[0])
             fetch_posts('index',1)
             
             document.getElementById("info").style.animation='none'
             document.getElementById("info").innerHTML=''
             setTimeout(()=>{
             document.getElementById("info").style.animation=''
             },0.5)

        })// restyle the element for next messages
        if(document.URL.indexOf("profile") == -1 && document.URL.indexOf("following") == -1) // this must be present on index only
        document.getElementById("form_post").onsubmit =()=>{
                save_post(true)
                return false
        }
        else if(document.URL.indexOf("profile") != -1){
        
        document.getElementById("profile_footer").addEventListener("click",(e)=>{
                 
                 if(e.target.tagName === 'BUTTON'){
                         if(e.target.getAttribute("id") === 'unFollowButton')
                         editUserStatus(e.target.dataset.id,false)
                         else
                         editUserStatus(e.target.dataset.id,true)
                         
                 }
        })

        }
             
        fetch_users("popular")
})
function editUserStatus(id,follow){

        fetch(`/editUserStatus/${id}`, {
                  method: 'PUT',
                  body: JSON.stringify({
                  follower : follow,
                })
        }).then((response)=>{if(response.ok){ return response.json();}  return null;}).then((response)=>{
            
            document.getElementById("Followers").innerHTML ="Followers:".concat(response["followers"])
            if(follow === false)
            {
               unFollowButton = document.getElementById("unFollowButton")
               unFollowButton.innerHTML = ''
               unFollowButton.setAttribute("id","followButton")
               unFollowButton.appendChild(document.createTextNode("Follow"))
               
            }
            else{
               
                followButton = document.getElementById("followButton")
                followButton.innerHTML = ''
                followButton.setAttribute("id","unFollowButton")
                followButton.appendChild(document.createTextNode("Un-Follow"))
                
            }
            
            fetch_users("popular")            
        }).catch(response=>{

                return console.log(response)
        }
        )



}
function getElm(element1,element2,attr){
       
        if(element1.getAttribute(attr))
        return element1
        else
        return element2
}
function runInfoTab(message,type){
        infoTab = document.getElementById("info")
        infoTab.className = type
        infoTab.innerHTML = ''
        infoTab.innerHTML = message
        info.style.animationPlayState ="running"
}
function like_post(id,liked){

        fetch(`/update_post/${id}`, {
                method: 'PUT',
                body: JSON.stringify({
                  like   : liked,
                })
        }).then((response)=>response.json()).then((response)=>{

            document.querySelector(`div[data-footer_id='${id}'] > #likes`).innerHTML = response["likes"]
            
        }).catch(response=>console.log(response))


}

function save_post(createPost,id){ // createPost  as well as edit post
                   
        fetch('/manage_post', {
                method: 'POST',
                body: JSON.stringify({
                    post       : createPost === true ?  document.getElementById("postInput").value : document.querySelector(`textarea[data-edit_input_id='${id}']`).value,
                    create_post: createPost,
                    post_id    : id
                })
              }).then((response)=>
              { if(response.url.includes("login")){//user is trying to post without login
                   flash = flashMessage[1];
                   runInfoTab("Login Required",messageDanger)
                   
                   return null
                }else{
                   if(createPost){
                   flash  = flashMessage[0];
                   runInfoTab("Posted",messageSuccess)
                   //fetch_posts("index",)
                   } 
                   return null;
                }
                
              })
              
}

function fetch_users(userType,searchValue){
        
        if(userType === 'popular'){
        document.getElementById("popularUser1").innerHTML = ''
        document.getElementById("popularUser2").innerHTML = ''
        document.getElementById("popularUser3").innerHTML = ''
        document.getElementById("popularUser4").innerHTML = ''
        document.getElementById("popularUser5").innerHTML = ''
        }
        else{
        document.getElementById("searchUser1").innerHTML = ''
        document.getElementById("searchUser2").innerHTML = ''
        document.getElementById("searchUser3").innerHTML = ''
        document.getElementById("searchUser4").innerHTML = ''
        document.getElementById("searchUser5").innerHTML = ''
        }
        fetch(`/fetch_users/${userType}?searchValue=${searchValue}`)
        .then(response=>response.json())
        .then((users) =>{ 
        users.forEach((user,index)=> {
        innerDiv                       = document.createElement('div')
        contentDiv                     = document.createElement('div')
        h6                             = document.createElement("h6")
        img                            = document.createElement('img')
        p1                             = document.createElement('p')
        a                              = document.createElement("a")
        p1.className                   = p1className
        a.className                    = headerClassName
        a.setAttribute("href",`/profile_view/${user.id}`)
        innerDiv.className             = innerDivClassName
        contentDiv.style.margin        = "0px 20px 0px 20px"
        img.className     = "rounded-circle"
        img.setAttribute("src",`https://avatars.dicebear.com/api/${user.avatar}/${user.seed}.svg`)
        img.setAttribute("width","70")
        img.setAttribute("height","70")
        h6.appendChild(document.createTextNode(user.username))
        p1.appendChild(document.createTextNode(`followers ${user.followers.length}    |   following ${user.following.length}`))
        a.appendChild(h6)
        contentDiv.append(a,p1)
        innerDiv.appendChild(img)
        innerDiv.appendChild(contentDiv)
        document.getElementById(`${userType}User${index+1}`).appendChild(innerDiv)
        })})

}
function htmlToElement(html) {
        var template = document.createElement('template');
        html = html.trim(); 
        template.innerHTML = html;
        return template.content.firstChild;
 }
function fetch_posts(page,page_number){
    
        document.getElementById("postTab").innerHTML=''
        fetch(`/fetch_posts/${page}?page=${page_number}`)
        .then(response => response.json())
        .then(posts => {  
        posts.forEach((post,index)=>{      
         mainDiv           = document.createElement('div')
         subDiv            = document.createElement('div')
         innerDiv          = document.createElement('div')
         contentDiv        = document.createElement('div')
         textDiv           = document.createElement('div')
         h6                = document.createElement("h6")
         p1                = document.createElement("p1")
         p2                = document.createElement("p2")
         a                 = document.createElement("a")
         a.setAttribute("href","#")
         a.className      = headerClassName
         h6.setAttribute("style",headerStyle)
         p1.className      = p1className
         p1.setAttribute("style",headerStyle)
         textDiv.className = p2className
         textDiv.setAttribute("style",p2style)
         footerDiv         = textDiv.cloneNode(true);
         mainDiv.className = mainDivClassName
         subDiv.className  = subDivClassName
         innerDiv.className= innerDivClassName
         img               = document.createElement('img')
         img.className     = "rounded-circle"
         img.setAttribute("src",`https://avatars.dicebear.com/api/${post.avatar}/${post.seed}.svg`)
         img.setAttribute("width","70")
         img.setAttribute("height","70")
         h6.appendChild(document.createTextNode(post.author))
         a.appendChild(h6)
         p1.appendChild(document.createTextNode("Shared publicly - " + post.timestamp))
         p2.appendChild(document.createTextNode(post.content))
         contentDiv.append(a,p1)
         innerDiv.appendChild(img)
         innerDiv.appendChild(contentDiv)
         textDiv.appendChild(p2)
         subDiv.append(innerDiv,textDiv)
         mainDiv.appendChild(subDiv)
         subDiv.appendChild(footerDiv)
         svg = htmlToElement(`<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="lightgrey" class="bi bi-heart" viewBox="0 0 16 16">
        <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/>
        </svg>`)
        likeCount = htmlToElement(`<span class="text-muted" id="likes" style="margin-left:10px;margin-right:15px;">0</span>`)
        likeCount.innerHTML = post.likes.length
        _ = (post.likes.indexOf(currentUser) === -1 ? null  : svg.setAttribute("fill","red"))
        footerDiv.append(svg,likeCount)
        if(currentUser === post.author){ // user has the ability to edit this post 
         button            = document.createElement("button")
         i                 = document.createElement("i")
         i.className       = "bi bi-pencil-square"
         button.className  = "btn btn-outline btn-sm"
         button.appendChild(i)
         footerDiv.appendChild(button)
        }
        //set animation for recent post and other default styles
       
         if(index === 0 && page_number ===1)
         mainDiv.setAttribute("id","recentPost")
         else
         mainDiv.setAttribute("id","post")

         // set id attributes for each post
         mainDiv.setAttribute("data-post_id",post.id)           
         footerDiv.setAttribute("data-footer_id",post.id)
         textDiv.setAttribute("data-content_id",post.id)
         document.getElementById("postTab").appendChild(mainDiv)


        })
                 
        

        });




}
