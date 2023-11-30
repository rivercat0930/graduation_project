// script.js
document.addEventListener('DOMContentLoaded', function() {
    // 獲取按鈕和隱藏元素的參考
    const showButton = document.getElementById('showButton');
    const hiddenElement = document.getElementById('hiddenElement');

    // 點擊按鈕時觸發的事件
    showButton.addEventListener('click', function () {
        // 切換隱藏元素的顯示狀態
        if (hiddenElement.style.display === 'none') {
            hiddenElement.style.display = 'block';
        } else {
            hiddenElement.style.display = 'block';
        }
    }
);
});







