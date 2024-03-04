function previewImage(event) {
    var input = event.target;
    var imagePreviewContainer = document.getElementById('image-preview-container');

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {

            var divElement = document.createElement('div');
            divElement.setAttribute('id', 'image-preview');
            divElement.style.backgroundImage = "url('" + e.target.result + "')";
            divElement.style.backgroundSize = "cover"; 
            divElement.style.backgroundPosition = 'center';
            divElement.style.backgroundRepeat = 'no-repeat';
            divElement.style.width = "200px";
            divElement.style.height = "200px";
            divElement.style.borderRadius = "10px";

            // 이미지 미리보기를 컨테이너에 삽입
            imagePreviewContainer.innerHTML = ''; // 이미지가 있을 경우 이전 이미지 제거
            imagePreviewContainer.appendChild(divElement);
        }

        reader.readAsDataURL(input.files[0]);
    } else {
        // 파일이 선택되지 않았을 때 이미지 미리보기 컨테이너를 비워줍니다.
        alert('이미지 없음');
    }

    setTimeout(function(){
        checkImagePreview();
    },50)
}
function checkImagePreview() {
    if ($('#image-preview-container').find('div').length > 0) {
        $('.photo_value_box').css({display: 'none'})
    }
}
