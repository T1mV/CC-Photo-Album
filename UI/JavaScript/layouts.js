const totalLayouts = 3;

let currentLayout = 1;
let isMirrored = false;

const albumContainer = document.querySelector(".album-container");
const previousButton = document.querySelector("#previous-layout");
const nextButton = document.querySelector("#next-layout");
const mirrorButton = document.querySelector("#mirror-layout");
const layoutIndicator = document.querySelector("#layout-indicator");


function updateLayout() {
    
    albumContainer.dataset.layout = currentLayout;
    albumContainer.dataset.mirrored = isMirrored;

    layoutIndicator.textContent = `Layout ${currentLayout}${isMirrored ? " (Mirrored" : ""}`;
    
    mirrorButton.textContent = isMirrored ? "Normal layout" : "Mirror layout";
}

nextButton.addEventListener("click", function() {

    currentLayout++;

    if (currentLayout > totalLayouts) {
        currentLayout = 1;
    }

    updateLayout();
})

previousButton.addEventListener("click", function() {

    currentLayout--;

    if (currentLayout < 1) {
        currentLayout = totalLayouts;
    }

    updateLayout();
})

mirrorButton.addEventListener("click", function() {
    
    isMirrored = !isMirrored
    updateLayout();

})

updateLayout();