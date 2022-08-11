//for each mail item in the mailbox
const mainDivClass = "d-flex justify-content-between hoverable p-2 mb-2 ";

// current mail that is loaded default values are assighned
currentMailId      =  0;
currentMailType    = "inbox";  
document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', (e) => { tab(e.target); load_mailbox('inbox'); });
  document.querySelector('#sent').addEventListener('click', (e) =>{tab(e.target);load_mailbox('sent')});
  document.querySelector('#archived').addEventListener('click', (e) => {tab(e.target);load_mailbox('archive')});
  document.querySelector('#compose').addEventListener('click', (e)=>{tab(e.target);compose_email()});
  document.querySelector('#Reply').addEventListener('click', (e)=>reply());//
  document.querySelector('#Archive').addEventListener('click', ()=>archive());//
  document.querySelector('form').onsubmit= ()=>{
  send_mail()
  return false;
  } //
  // add event listener for emails-view div 
  document.querySelector('#emails-view').addEventListener('click',(e)=>{
  target = e.target
  while(target.dataset.email_id === undefined){
    target = target.parentNode
  } //buble outwards till find an elemnt with data-email_id value then call load_mail()
  currentMailId   = target.dataset.email_id;
  currentMailType = target.dataset.type;
  load_mail()
  });
  
  // By default, load the inbox
  load_mailbox('inbox');
});
function reply(){
  recipientsField = document.getElementById('compose-recipients');
  subjectField    = document.getElementById('compose-subject');
  bodyField       = document.getElementById('compose-body');
  fetch(`/emails/${currentMailId}`)
.then(response => response.json())
.then(email => {
 recipientsField.value   = email.sender;
 subjectField.value = (email.subject.slice(0,3) === "Re:" ? email.subject : "Re: ".concat(email.subject));  
 bodyField.value    =`On ${email.timestamp} ${email.sender} wrote: \n\n`.concat(email.body).concat("\n\n");
});
 
 return  document.getElementById('compose').click();

}
function archive(){
  
  Archive = true;
  if(currentMailType === 'archive')
  Archive = false;


  fetch(`/emails/${currentMailId}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: Archive
    })
  }).then(()=>{document.getElementById('inbox').click();})
}
function send_mail(){
  
  recipientsField = document.getElementById('compose-recipients');
  subjectField    = document.getElementById('compose-subject');
  bodyField       = document.getElementById('compose-body');
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipientsField.value,
        subject:subjectField.value,
        body: bodyField.value
    })
  })
  .then(response => {
   
  if(response.status == 201){
  document.getElementById('sent').click();//simulate the click of sent tab
  return null
  }
  return response.json()
  }).then((result)=>{

     document.getElementById('info').style.display = 'block'
     document.getElementById('info').innerHTML = result.error;
     recipientsField.style.border = "1px solid red";
    
  })
  
}
function tab(target){

  document.querySelectorAll("li button").forEach((elm)=>{
  
    elm.setAttribute('class','nav-link')
    elm.setAttribute('aria-selected','false')})
  
    target.setAttribute('class','nav-link active')
    target.setAttribute('aria-selected','true')
}
function compose_email() {
  // hide error prompt
  document.getElementById('info').innerHTML='';
  document.getElementById('info').style.display = 'none';
  document.getElementById('compose-recipients').style.border = "1px solid lightgrey"
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.getElementById('compose-recipients').value = '';
  document.getElementById('compose-subject').value    = '';
  document.getElementById('compose-body').value       = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').innerHTML='';
  // Show the mailbox contents

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach((email)=>{
    badge      =  document.createElement('span');
    mainDiv    =  document.createElement('div');
    authorDiv  =  document.createElement('div');
    subjectDiv =  document.createElement('div');
    bodySpan   =  document.createElement('span');
    timeStamp  =  document.createElement('div');
    badge.className      = "badge rounded-pill bg-danger ms-2";
    authorDiv.className  = "fw-bold";
    subjectDiv.className = "fw-bold me-auto ms-5";
    timeStamp.className  = "text-muted";
    bodySpan.className   = "fw-normal";
    mainDiv.className    =  mainDivClass;
    badge.innerHTML      = 'New';
    mainDiv.setAttribute("data-email_id",`${email.id}`);
    mainDiv.setAttribute("data-type",`${mailbox}`);
    authorDiv.appendChild(document.createTextNode(email.sender))
    subjectDiv.appendChild(document.createTextNode(email.subject))
    //attach badge
    if(email.read == true){
      mainDiv.style.background = "rgb(210, 210, 210)";
    }
    else
    authorDiv.appendChild(badge);
    
    bodySpan.appendChild(document.createTextNode(" - "+email.body.slice(0,60)))
    timeStamp.appendChild(document.createTextNode(email.timestamp))
    subjectDiv.appendChild(bodySpan)
    mainDiv.appendChild(authorDiv)
    mainDiv.appendChild(subjectDiv)
    mainDiv.appendChild(timeStamp)
    document.getElementById("emails-view").appendChild(mainDiv)
   
   })
      
    });
}
function load_mail(){
document.querySelector('#Archive').style.display      = 'inline';
document.querySelector('#emails-view').style.display  = 'none';
document.querySelector('#compose-view').style.display = 'none';
document.querySelector('#email-view').style.display   = 'block';
if(currentMailType === "sent")
document.querySelector('#Archive').style.display      = 'none';
else if(currentMailType === "archive")
document.querySelector('#Archive').innerHTML          = 'Un-Archive';
else
document.querySelector('#Archive').innerHTML          = 'Archive';


document.querySelectorAll("li > span").forEach((span)=>{
   
   if(span.nextSibling !== null )
   span.parentNode.removeChild(span.nextSibling);

})
document.querySelector('#body').innerHTML = '';
//make a request to the api
fetch(`/emails/${currentMailId}`)
.then(response => response.json())
.then(email => {
    
  document.getElementById("from").appendChild(document.createTextNode(email.sender))
  document.getElementById("to").appendChild(document.createTextNode(email.recipients.toString()))
  document.getElementById("subject").appendChild(document.createTextNode(email.subject))
  document.getElementById("timestamp").appendChild(document.createTextNode(email.timestamp))
  document.getElementById("body").appendChild(document.createTextNode(email.body))
  
});
//mark the mail as seen
  fetch(`/emails/${currentMailId}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })


}
