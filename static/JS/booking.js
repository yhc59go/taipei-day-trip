window.onload=function(){
    checkLogin();
    getBookinInfo();
    getUserInfo()
    
}
function checkLogin(){
    let src="/api/user/auth";
    fetch(src,
            {
                method:"GET",
                headers:{"Content-Type": "application/json"},
            }
    ).then(response => response.json())
    .then(function(data){
            if(data.data){
                userData=JSON.parse(data.data);
                let greedingMessageBlock=document.getElementById("greedingMessage");    
                greedingMessage=greedingMessageBlock.textContent;
                greedingMessage=greedingMessage.replace("，", "，"+userData.name+"，");
                greedingMessageBlock.textContent=greedingMessage;
            }else{
                location.href="/";
            }
        }
    ); 
}

function getBookinInfo(){
    let src="/api/booking";
    fetch(src,
            {
                method:"GET",
                headers:{"Content-Type": "application/json"},
            }
    ).then(response => response.json())
    .then(function(data){
            const getBookingInformation=document.getElementById("getBookingInformation");
            const noBookingInformation=document.getElementById("noBookingInformation");
            if(data.data){
                getBookingInformation.style.display="block";
                noBookingInformation.style.display="none";
                bookingData=data.data;
                bookingAttraction=JSON.parse(bookingData.attraction);
                //Get attraction image
                let attractionImageInbookingPage=document.getElementById('attractionImage');
                attractionImageInbookingPage.style.backgroundImage = "url('" + bookingAttraction.image+ "')"; 
                //Get attraction name
                let bookAttractionInBookingPage=document.getElementById('bookAttractionInBookingPage');
                bookAttractionInBookingPage.textContent=bookingAttraction.name;
                //Get booking date
                let bookDateInBookingPage=document.getElementById('bookDateInBookingPage');
                bookDateInBookingPage.textContent=bookingData.date;
                //Get time and cost
                let bookTimeInBookingPage=document.getElementById('bookTimeInBookingPage');
                let bookCostInBookingPage=document.getElementById('bookCostInBookingPage');
                let totalCostInBookingPage=document.getElementById('totalCostInBookingPage');
                if(bookingData.time=="morning"){
                    bookTimeInBookingPage.textContent="早上九點到下午四點";
                    bookCostInBookingPage.textContent="新台幣 2000 元";
                    totalCostInBookingPage.textContent="新台幣 2000 元";
                }else if(bookingData.time=="afternoon"){
                    bookTimeInBookingPage.textContent="下午五點到晚上九點";
                    bookCostInBookingPage.textContent="新台幣 2500 元";
                    totalCostInBookingPage.textContent="新台幣 2500 元";
                }         
                //Get address
                let bookAddressInBookingPage=document.getElementById('bookAddressInBookingPage');
                bookAddressInBookingPage.textContent=bookingAttraction.address;
            }else{
                getBookingInformation.style.display="none";
                noBookingInformation.style.display="block";
            }
        }
    ); 
}

function getUserInfo(){
    let src="/api/user/auth";
    fetch(src,
            {
                method:"GET",
                headers:{"Content-Type": "application/json"},
            }
    ).then(response => response.json())
    .then(function(data){
            if(data.data){
                let userInfo=JSON.parse(data.data);
                //Get username
                let contactName=document.getElementById('contactName');
                contactName.value=userInfo.name;
                //Get user's mail
                let contactMail=document.getElementById('contactMail');
                contactMail.value=userInfo.email;
            }else{
                console.log(data.data);
            }
        }
    ); 
}
const deleteIcon=document.getElementById("deleteIcon");
deleteIcon.addEventListener("click", deleteBooking);
function deleteBooking(){
    let src="/api/booking";
    fetch(src,
            {
                method:"DELETE",
                headers:{"Content-Type": "application/json"},
            }
    ).then(response => response.json())
    .then(function(data){
            if(data.ok==true){
                location.href="/booking";
            }else if(data.error==true){
                console.log(data.message);
            }
        }
    ); 
}