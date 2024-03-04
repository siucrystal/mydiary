$(document).ready(function(){
    var burger = $('.ham_icon_box');

    burger.each(function(index){
        var $this = $(this);
        console.log('this : ', $this)
    
        $this.on('click', function(e){
            e.preventDefault();
            $(this).toggleClass('active-ham');
            $('.ham_menu_box').toggleClass('activate_ham_menu')
        })
    });
})