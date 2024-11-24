const initVMasker = (root) => {
    const selector = 'input[data-mask]';
    const inputs = Array.from(root.querySelectorAll(selector));

    for (const input of inputs) {
        const maskPattern = input.getAttribute('data-mask');
        VMasker(input).maskPattern(maskPattern);
    }
}

document.addEventListener('DOMContentLoaded', function(){
    initVMasker(document);
});
