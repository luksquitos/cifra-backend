function handleClosePreviewWindow(e) {
    e.preventDefault();
    e.stopPropagation();

    const script = document.createElement('script');
    script.dataset.popupResponse = JSON.stringify({
        action: 'change',
        value: {},
        obj: {},
        new_value: {},
    });
    script.id = 'django-admin-popup-response-constants';
    script.src = '/static/admin/js/popup_response.js'

    document.head.appendChild(script);
}

document.addEventListener('DOMContentLoaded', function() {
    if (!window.location.search.includes('_popup=1')) {
        return;
    }

    Array.from(document.querySelectorAll('.closelink')).forEach((item) => {
        item.addEventListener('click', handleClosePreviewWindow);
    });
});
