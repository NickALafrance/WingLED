import _ from 'lodash';

import { hexToHsv, hsvToHex } from '../../util';

/**
 * @class Color
 * @classdesc helper class for controlling color.  Can auto convert from hsv to hex and back.
 */
class Color {
    /**
     * get hue
     * @return {Number}
     */
    get hue() {
        return this._hue;
    }
    /**
     * set hue
     * @param {Number} h [0 - 360]
     */
    set hue(h) {
        this._hue = h % 360;
    }

    /**
     * get Saturation
     * @return {Number}
     */
    get saturation() {
        return this._saturation;
    }
    /**
     * set saturation
     * @param {Number} s [0 - 1]
     */
    set saturation(s) {
        this._saturation = Math.round(Math.max(0, Math.min(1, s)) * 100) / 100;
    }

    /**
     * get Value
     * @return {Number}
     */
    get value() {
        return this._value;
    }
    /**
     * set value
     * @param {Number} v [0 - 1]
     */
    set value(v) {
        this._value = Math.round(Math.max(0, Math.min(1, v)) * 100) / 100;
    }

    /**
     * returns the hex representation of this color
     * @return {string}
     */
    get hex() {
        return hsvToHex(this.hue, this.saturation, this.value);
    }
    /**
     * Alias for setColor.
     * @param {string} hex
     */
    set hex(hex) {
        this.setColor(hex);
    }
    /**
     * Color constructor.  Default to red.
     * @param {Number|string|object|array} h
     * @param {Number} s
     * @param {Number} v
     */
    constructor(h = 0, s = 1, v = 1) {
        this.setColor(h, s, v);
    }

    /**
     * set color.  Can take either hsv or hex.
     * Can take an object with keys hue, saturation, value
     * Can take an array [hue,. saturation, value]
     * @param {Number|string|object|array} h
     * @param {Number} s
     * @param {Number} v
     */
    setColor(h, s = null, v = null) {
        if (_.isString(h)) {
            const hsv = hexToHsv(h);
            this.hue = hsv.hue;
            this.saturation = hsv.saturation;
            this.value = hsv.value;
        } else if (_.isArray(h)) {
            this.hue = h[0];
            this.saturation = h[1];
            this.value = h[2];
        } else if (_.isObject(h)) {
            this.hue = _.get(h, 'hue', 0);
            this.saturation = _.get(h, 'saturation', 1);
            this.value = _.get(h, 'value', 1);
        } else if (_.isNumber(h)) {
            this.hue = h;
            this.saturation = s;
            this.value = v;
        }
    }

    /**
     * Returns the HSV for the color as an object.
     * @return {{hue: Number, saturation: Number, value: Number}}
     */
    toObject() {
        return {
            hue: this.hue,
            saturation: this.saturation,
            value: this.value,
        };
    }

    /**
     * Returns color as an array.
     * @return {array}
     */
    toArray() {
        return [this.hue, this.saturation, this.value];
    }
}

export default Color;
