function generateRandomKey() {
    let key = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+';
    for (let i = 0; i < 20; i++) {
        key += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    document.getElementById('key').value = key;
}

function fileSelected() {
    let fileInput = document.getElementById('file-input');
    let file = fileInput.files[0];

    if (file) {
        if (file.size > 200 * 1024 * 1024) {
            alert('ファイルが大きすぎます。200MB以下のファイルを選択してください。');
            return; // これ以上の処理を中断
        }
        // ファイル情報の表示
        document.getElementById('file-name').textContent = file.name;
        // document.getElementById('file-meta').textContent = `${(file.size / 1024).toFixed(2)} KB - ${file.type}`;
        document.getElementById('file-meta').textContent = `${(file.size / 1024).toFixed(2)} KB`;
        document.getElementById('file-type').textContent = `${file.type}`;
        document.getElementById('file-icon').src = './static/img/file-icon.png'; // ファイルタイプに基づいてアイコンを設定

        // ファイル情報エリアを表示
        document.getElementById('file-info').style.display = 'flex';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('drop-area').addEventListener('click', function() {
        document.getElementById('file-input').click();
    });
    
    document.getElementById('drop-area').addEventListener('dragover', function(event) {
        event.preventDefault();
        event.stopPropagation();
        this.style.border = '2px solid #000';  // ドラッグ中のスタイル変更
    });
    
    document.getElementById('drop-area').addEventListener('dragleave', function(event) {
        event.preventDefault();
        event.stopPropagation();
        this.style.border = '2px dashed #ccc';  // ドラッグが終わった時のスタイルに戻す
    });
    
    document.getElementById('drop-area').addEventListener('drop', function(event) {
        event.preventDefault();
        event.stopPropagation();
        this.style.border = '2px dashed #ccc';  // ドロップ後のスタイルに戻す
        let files = event.dataTransfer.files;
        if (files.length) {
            document.getElementById('file-input').files = files;
            // document.getElementById('upload-form').submit(); // フォームを自動でサブミット
            fileSelected();
        }
    });
    
});