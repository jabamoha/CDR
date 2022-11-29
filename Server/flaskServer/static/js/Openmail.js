
$(document).ready(function(){

    const btns=document.querySelectorAll('.d');
    btns.forEach(btn => {
        btn.addEventListener('click', function handleClick(event) {
          console.log('box clicked', event);
          let id=event.target.id;

          document.getElementsByName(id)[0].submit();
          $('form[name='+id).submit(function (e){

            e.preventDefault();

            



          });




          
      
        });
      });
});


