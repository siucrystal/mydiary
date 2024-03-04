$(document).ready(function(){
    $(document).on('click', function(event) {
        // 클릭된 요소가 ul 요소인지 확인
        if (!$(event.target).closest('.date_text').length) {
            // ul 요소 외의 다른 요소가 클릭되었을 때
            $('.from_ul').css('display', 'none');
        }
        if (!$(event.target).closest('#mood').length) {
            // ul 요소 외의 다른 요소가 클릭되었을 때
            $('#mood').css({
                background: 'transparent',
                borderBottom: '2px solid transparent'
            })
        }
        if (!$(event.target).closest('#weather').length) {
            // ul 요소 외의 다른 요소가 클릭되었을 때
            $('#weather').css({
                background: 'transparent',
                borderBottom: '2px solid transparent'
            })
        }
        if (!$(event.target).closest('.title_box input').length) {
            // ul 요소 외의 다른 요소가 클릭되었을 때
            $('.title_box input').css({
                background: 'transparent',
                border: '2px solid #ddd'
            })
        }
        if (!$(event.target).closest('.content_box textarea').length) {
            // ul 요소 외의 다른 요소가 클릭되었을 때
            $('.content_box textarea').css({
                background: 'transparent',
                border: '2px solid #ddd'
            })
        }
    });

    $('.date_text').on('click',function(){
        var $date_text = $(this); // 클릭된 요소를 jQuery 객체로 가져옵니다.
        var $span = $date_text.find('span'); // 클릭된 요소의 자식 span 요소를 가져옵니다.
        var date_text = $span.text(); // span 요소의 텍스트를 가져옵니다.
        var $from_ul = $date_text.siblings('.from_ul');

        $from_ul.css('display', 'flex');

        $from_ul.find('li').on('click', function() {
            var text = $(this).text();
            $span.text(text); // 클릭된 li의 텍스트를 span 요소에 설정합니다.
        });
    })

    $('#weather, #mood').on('click', function() {
        $(this).css({
            background: '#F4FAFF',
            borderBottom: '2px solid #B0D9FF'
        })
    });

    $('.title_box input, .content_box textarea').on('click', function() {
        $(this).css({
            background: '#F4FAFF',
            border: '2px solid #B0D9FF'
        })
    });




})