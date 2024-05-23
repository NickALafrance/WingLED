/**
 * Extract the ID from a link.
 * @param {*} link
 * @return {string}
 */
export function getPositionFromLink(link) {
    return parseInt(link.split('/').pop());
}

/**
 * Convert HSV to hexadecimal
 * @param {Number} h
 * @param {Number} s
 * @param {Number} v
 * @return {string}
 */
export function hsvToHex(h, s, v) {
    // Ensure the HSV values are in the correct range
    h = h % 360;
    s = Math.min(Math.max(s, 0), 1);
    v = Math.min(Math.max(v, 0), 1);

    const c = v * s;
    const x = c * (1 - Math.abs((h / 60) % 2 - 1));
    const m = v - c;
    let r; let g; let b;

    if (0 <= h && h < 60) {
        r = c;
        g = x;
        b = 0;
    } else if (60 <= h && h < 120) {
        r = x;
        g = c;
        b = 0;
    } else if (120 <= h && h < 180) {
        r = 0;
        g = c;
        b = x;
    } else if (180 <= h && h < 240) {
        r = 0;
        g = x;
        b = c;
    } else if (240 <= h && h < 300) {
        r = x;
        g = 0;
        b = c;
    } else {
        r = c;
        g = 0;
        b = x;
    }

    // Convert RGB to [0, 255] range and add m to each component
    r = Math.round((r + m) * 255);
    g = Math.round((g + m) * 255);
    b = Math.round((b + m) * 255);

    // Convert RGB to hex
    const rgbToHex = (component) => {
        const hex = component.toString(16);
        return hex.length === 1 ? '0' + hex : hex;
    };

    return `#${rgbToHex(r)}${rgbToHex(g)}${rgbToHex(b)}`;
}

/**
 * returns the HSV representation of a hex number
 * @param {string} hex
 * @return {object}
 */
export function hexToHsv(hex) {
    // Ensure the hex string starts with '#' and remove it
    if (hex.startsWith('#')) {
        hex = hex.slice(1);
    }

    // Parse the r, g, b values from the hex string
    const r = parseInt(hex.slice(0, 2), 16) / 255;
    const g = parseInt(hex.slice(2, 4), 16) / 255;
    const b = parseInt(hex.slice(4, 6), 16) / 255;

    const max = Math.max(r, g, b); const min = Math.min(r, g, b);
    let h; let s; let v = max;

    const d = max - min;
    s = max === 0 ? 0 : d / max;

    if (max === min) {
        h = 0; // achromatic
    } else {
        switch (max) {
        case r:
            h = (g - b) / d + (g < b ? 6 : 0);
            break;
        case g:
            h = (b - r) / d + 2;
            break;
        case b:
            h = (r - g) / d + 4;
            break;
        }
        h /= 6;
    }

    h = Math.round(h * 360);
    s = Math.round(s * 100) / 100;
    v = Math.round(v * 100) / 100;

    return { hue: h, saturation: s, value: v };
}
