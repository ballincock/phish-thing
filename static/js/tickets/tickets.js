const replyarea = document.getElementById('replyMsg');
replyarea.addEventListener('input', function() {
    const remaining = 1000 - this.value.length;
    document.getElementById('replyCount').textContent = remaining + " characters remaining";
});

const textarea = document.getElementById('ticketMsg');
if(textarea) {
    textarea.addEventListener('input', function() {
        const remaining = 1000 - this.value.length;
        document.getElementById('charCount').textContent = remaining + " characters remaining";
    });
}
