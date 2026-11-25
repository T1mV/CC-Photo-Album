const themes = {

    vintage: {
        background: "#d8cfc0",
        cover: "#a99579",
        leftPage: "#f7f1e5",
        rightPage: "#fbf7ee",
        text: "#514638",
        muted: "#806f5b",
        accent: "#92785b",
        border: "#d8cdbb",
        controls: "#f8f3e9",
        spine: "rgba(80, 60, 40, 0.18)"
    },

    nature: {
        background: "#c9d2bd",
        cover: "#899b78",
        leftPage: "#eef1e5",
        rightPage: "#f5f7ed",
        text: "#3f5039",
        muted: "#718265",
        accent: "#71865d",
        border: "#d0d9c4",
        controls: "#f0f3e8",
        spine: "rgba(48, 70, 42, 0.18)"
    },

    dreamy: {
        background: "#d9cde0",
        cover: "#a995b8",
        leftPage: "#f3eefa",
        rightPage: "#faf5fc",
        text: "#55445f",
        muted: "#887493",
        accent: "#987fa8",
        border: "#e0d5e9",
        controls: "#f8f2fb",
        spine: "rgba(82, 59, 96, 0.18)"
    },

    minimalist: {
        background: "#dedede",
        cover: "#a8a8a8",
        leftPage: "#f5f5f5",
        rightPage: "#ffffff",
        text: "#333333",
        muted: "#777777",
        accent: "#777777",
        border: "#dddddd",
        controls: "#f5f5f5",
        spine: "rgba(0, 0, 0, 0.15)"
    },

    city: {
        background: "#bfc5ce",
        cover: "#747f90",
        leftPage: "#e9ebef",
        rightPage: "#f4f5f7",
        text: "#343d4a",
        muted: "#687486",
        accent: "#586779",
        border: "#d0d4dc",
        controls: "#f0f1f4",
        spine: "rgba(35, 45, 60, 0.2)"
    },

    summer: {
        background: "#f0d49e",
        cover: "#d6a85e",
        leftPage: "#fff2d6",
        rightPage: "#fff8e8",
        text: "#76502b",
        muted: "#a47a43",
        accent: "#c28c3f",
        border: "#f0dfbb",
        controls: "#fff4dd",
        spine: "rgba(120, 75, 25, 0.16)"
    },

    spring: {
        background: "#d5dfc5",
        cover: "#a5b98d",
        leftPage: "#f0f3e6",
        rightPage: "#f8f8ef",
        text: "#4c6042",
        muted: "#82936f",
        accent: "#91a875",
        border: "#dce5d0",
        controls: "#f4f6eb",
        spine: "rgba(60, 85, 45, 0.16)"
    },

    autumn: {
        background: "#d5b99c",
        cover: "#a87851",
        leftPage: "#f2e5d3",
        rightPage: "#f8eee0",
        text: "#65452f",
        muted: "#977253",
        accent: "#a56e43",
        border: "#e4d1b9",
        controls: "#f5e8d6",
        spine: "rgba(90, 50, 25, 0.2)"
    },

    winter: {
        background: "#c7d4df",
        cover: "#849aaa",
        leftPage: "#edf3f7",
        rightPage: "#f7fafc",
        text: "#3e5363",
        muted: "#718899",
        accent: "#7794a8",
        border: "#d5e0e8",
        controls: "#f1f6f9",
        spine: "rgba(45, 70, 90, 0.18)"
    },

    beach: {
        background: "#c5d9d6",
        cover: "#7daaa3",
        leftPage: "#f2ead8",
        rightPage: "#fff8e9",
        text: "#3d625e",
        muted: "#77958e",
        accent: "#6e9d95",
        border: "#e1e2d3",
        controls: "#f8f2e4",
        spine: "rgba(45, 95, 85, 0.16)"
    }

};


const themeDecorations = {

    vintage: {
        left: [
            { symbol: "📮", size: "large", top: "3%", right: "5%" },
            { symbol: "✉️", size: "small", bottom: "4%", left: "5%" }
        ],
        right: [
            { symbol: "🌼", size: "large", top: "4%", right: "5%" },
            { symbol: "🏷️", size: "small", bottom: "4%", right: "5%" }
        ]
    },

    nature: {
        left: [
            { symbol: "🌿", size: "large", top: "3%", right: "5%" },
            { symbol: "🍃", size: "small", bottom: "4%", left: "5%" }
        ],
        right: [
            { symbol: "🌸", size: "large", top: "4%", right: "5%" },
            { symbol: "🦋", size: "small", bottom: "4%", right: "5%" }
        ]
    },

    dreamy: {
        left: [
            { symbol: "☁️", size: "large", top: "3%", right: "5%" },
            { symbol: "✨", size: "small", bottom: "4%", left: "5%" }
        ],
        right: [
            { symbol: "🌙", size: "large", top: "4%", right: "5%" },
            { symbol: "⭐", size: "small", bottom: "4%", right: "5%" }
        ]
    },

    minimalist: {
        left: [
            { symbol: "◯", size: "large", top: "3%", right: "5%" },
            { symbol: "◇", size: "small", bottom: "4%", left: "5%" }
        ],
        right: [
            { symbol: "□", size: "large", top: "4%", right: "5%" },
            { symbol: "·", size: "small", bottom: "4%", right: "5%" }
        ]
    },

    city: {
        left: [
            { symbol: "🏙️", size: "large", top: "3%", right: "5%" },
            { symbol: "🚇", size: "small", bottom: "4%", left: "5%" }
        ],
        right: [
            { symbol: "📍", size: "large", top: "4%", right: "5%" },
            { symbol: "🚕", size: "small", bottom: "4%", right: "5%" }
        ]
    },

    summer: {
        left: [
            { symbol: "☀️", size: "large", top: "3%", right: "5%" },
            { symbol: "🍋", size: "small", bottom: "4%", left: "5%" }
        ],
        right: [
            { symbol: "🍉", size: "large", top: "4%", right: "5%" },
            { symbol: "🌻", size: "small", bottom: "4%", right: "5%" }
        ]
    },

    spring: {
        left: [
            { symbol: "🌷", size: "large", top: "3%", right: "5%" },
            { symbol: "🌼", size: "small", bottom: "4%", left: "5%" }
        ],
        right: [
            { symbol: "🦋", size: "large", top: "4%", right: "5%" },
            { symbol: "🐝", size: "small", bottom: "4%", right: "5%" }
        ]
    },

    autumn: {
        left: [
            { symbol: "🍂", size: "large", top: "3%", right: "5%" },
            { symbol: "🌰", size: "small", bottom: "4%", left: "5%" }
        ],
        right: [
            { symbol: "🎃", size: "large", top: "4%", right: "5%" },
            { symbol: "🍁", size: "small", bottom: "4%", right: "5%" }
        ]
    },

    winter: {
        left: [
            { symbol: "❄️", size: "large", top: "3%", right: "5%" },
            { symbol: "✨", size: "small", bottom: "4%", left: "5%" }
        ],
        right: [
            { symbol: "⛄", size: "large", top: "4%", right: "5%" },
            { symbol: "🧤", size: "small", bottom: "4%", right: "5%" }
        ]
    },

    beach: {
        left: [
            { symbol: "🐚", size: "large", top: "3%", right: "5%" },
            { symbol: "⭐", size: "small", bottom: "4%", left: "5%" }
        ],
        right: [
            { symbol: "🌴", size: "large", top: "4%", right: "5%" },
            { symbol: "🌊", size: "small", bottom: "4%", right: "5%" }
        ]
    }

};



function renderDecorations(themeName) {

    const decorations = themeDecorations[themeName];

    const leftContainer = document.querySelector(".left-decorations");
    const rightContainer = document.querySelector(".right-decorations");

    leftContainer.innerHTML = "";
    rightContainer.innerHTML = "";

    function addStickers(container, stickers) {

        stickers.forEach(function(stickerData) {

            const sticker = document.createElement("span");

            sticker.className = `sticker sticker-${stickerData.size}`;
            sticker.textContent = stickerData.symbol;

            if (stickerData.top) {
                sticker.style.top = stickerData.top;
            }

            if (stickerData.bottom) {
                sticker.style.bottom = stickerData.bottom;
            }

            if (stickerData.left) {
                sticker.style.left = stickerData.left;
            }

            if (stickerData.right) {
                sticker.style.right = stickerData.right;
            }

            container.appendChild(sticker);

        });

    }

    addStickers(leftContainer, decorations.left);
    addStickers(rightContainer, decorations.right);

}


function applyTheme(themeName) {

    const theme = themes[themeName];
    document.documentElement.dataset.theme = themeName;
    const root = document.documentElement; 

    root.style.setProperty("--background", theme.background);
    root.style.setProperty("--cover", theme.cover);
    root.style.setProperty("--left-page", theme.leftPage);
    root.style.setProperty("--right-page", theme.rightPage);
    root.style.setProperty("--text", theme.text);
    root.style.setProperty("--muted", theme.muted);
    root.style.setProperty("--accent", theme.accent);
    root.style.setProperty("--border", theme.border);
    root.style.setProperty("--controls", theme.controls);
    root.style.setProperty("--spine", theme.spine);
    renderDecorations(themeName);
}

const themeSelector = document.querySelector("#theme-selector");

themeSelector.addEventListener("change", function() {
    
    const selectedTheme = themeSelector.value;
    applyTheme(selectedTheme);

})

applyTheme("vintage");