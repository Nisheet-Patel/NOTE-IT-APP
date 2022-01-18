function copyToClipboard(value) {
    navigator.clipboard.writeText(value);
    
    /* Alert the copied text */
    alert("Public Link Copied Successfully");
}