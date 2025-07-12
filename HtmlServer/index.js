const submitBtn = document.getElementById('submit');
const emailInput = document.getElementById('email');
const image = document.getElementById('image');
const imageTitle = document.getElementById('imageTitle');

document.addEventListener("DOMContentLoaded", function(event) { 
    //Check if image was able to be loaded
    image.addEventListener('load', () => {
        console.log("Image loaded")
    })
    //Check if image was not able to be loaded
    image.addEventListener('error', () => {
        console.log("Image not loaded")
        imageTitle.innerHTML = "Please take a picture with the Jovi to see it here!"
        image.remove()
    })
});

submitBtn.addEventListener('click', async (e) => {
    e.preventDefault(); // Stop the page from refreshing

    const email = emailInput.value;

    fetch('http://192.168.1.16:8080/set_email/' + email,{
      
    })
        .then(async (response) => {
            if (!response.ok) {
                alert("Error");
                throw new Error(response.error);
            }
            
            console.log(response    )
            //Object to string
            data = await response.json()
            emailStatus = data.status
            if (emailStatus == "set_email"){
                alert("Email set, Now take a picture with the jovi!")
            }
            if (emailStatus == "email_sent"){
                alert("Photo sent to your email!")
                emailInput.value = ""
            }

            // alert(response.text)
            // Wait 10 seconds before sending the next request
            
                return response;
        
        })
        
});

function objToString(obj){
    var str = '';
    for (var p in obj) {
        str += p + '::' + obj[p] + '\n';
        if (obj.hasOwnProperty(p)) {
            str += p + '::' + obj[p] + '\n';
        }
    }
    return str;
}