// Initialize Mermaid diagrams
document.addEventListener('DOMContentLoaded', function() {
    if (typeof mermaid !== 'undefined') {
        mermaid.initialize({
            startOnLoad: true,
            theme: 'default',
            flowchart: {
                useMaxWidth: true,
                htmlLabels: true
            },
            sequence: {
                useMaxWidth: true
            }
        });

        // Convert code blocks with mermaid syntax to mermaid divs
        document.querySelectorAll('.highlight-mermaid pre').forEach(function(pre) {
            const container = document.createElement('div');
            container.className = 'mermaid';
            container.textContent = pre.textContent;
            pre.parentElement.replaceChild(container, pre);
        });

        // Re-run mermaid on any new diagrams
        mermaid.run();
    }
});