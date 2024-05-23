import _ from 'lodash';

import Color from '../Color';
import JumpStrategy from './JumpStrategy';

/**
 * n1 approaches n2 by % amount.
 * @param {Number} n1
 * @param {Number} n2
 * @param {Number} percent
 * @return {Number}
 */
function approach(n1, n2, percent) {
    if (n1 === n2) {
        return n1;
    }
    const diff = Math.abs((n1 - n2) * percent);
    if (n1 > n2) {
        return n1 - diff;
    }
    return n1 + diff;
}

/**
 * Preform a clocokwise hue rotation
 * @param {Number} n1
 * @param {Number} n2
 * @param {Number} percent
 * @return {Number}
 */
function clockwiseHueRotation(n1, n2, percent) {
    if (n1 === n2) {
        return n1;
    }
    if (n1 > n2) {
        n2 += 360;
    }
    const diff = (n2 - n1) * percent;
    return (n1 + diff) % 360;
}

/**
 * Preform a counterclocokwise hue rotation
 * @param {Number} n1
 * @param {Number} n2
 * @param {Number} percent
 * @return {Number}
 */
function counterclockwiseHueRotation(n1, n2, percent) {
    if (n1 === n2) {
        return n1;
    }
    if (n1 < n2) {
        n1 += 360;
    }
    const diff = (n1 - n2) * percent;
    return (n1 - diff) % 360;
}

/**
 * @class FadeStrategy
 * @classdesc This strategy will fade the current color to the next color,
 *  making one step per BPM towards the next color. It uses four parameters, colors, function, stepCount, and clockwise
 *  COLORS should be an array of tuples, where each tuple is 1 integer between 0 and 360 for Hue,
 *  and 2 floats between 0 and 1 for Saturation and Value.
 *  The function is a string that should be one of the ways to fade from one color to the next.
 *  The enumerations are as follows: 'linear', 'gaussian'
 *  The stepCount is how many steps should it take to fade from one color to the next.
 *  clockwise is a boolean and will represent which direction the fade is going along the color
 *  wheel for hue, and wether its increasing or decreaing between 0 and 1 for S and V
 *  Example of options ->
 *{
 *    type: "Fade",
 *    colors: [
 *        [0, 1, 1],   # RED
 *        [120, 1, 1], # GREEN
 *        [240, 1, 1]  # BLUE
 *    ],
 *    function: "linear", # OPTIONAL, defaults to linear
 *    steps: 10, # OPTIONAL, defaults to 10
 *    clockwise: true # OPTIONAL, defaults to True
 *}
 */
class FadeStrategy extends JumpStrategy {
    /**
     * constructor
     * @param {object} config
     */
    constructor(config) {
        super(config);
        this.function = _.get(config, 'function', 'linear');
        this.steps = _.get(config, 'steps', 10);
        this.clockwise = _.get(config, 'clockwise', true);
    }

    /**
     * Get next color
     * @return {string}
     */
    getNextColor() {
        if (_.isNil(this.currentColor)) {
            this.currentColor = 0;
            this.currentStep = 0;
        }
        this.currentStep++;
        if (this.currentStep === this.steps) {
            this.currentColor++;
            this.currentStep = 0;
            return this.colors[this.currentColor % this.colors.length].hex;
        }
        const c1 = this.colors[this.currentColor % this.colors.length];
        const c2 = this.colors[(this.currentColor + 1) % this.colors.length];
        const percent = this.currentStep / this.steps;

        const nextColor = new Color(
            this.clockwise ? clockwiseHueRotation(c1.hue, c2.hue, percent) :
                counterclockwiseHueRotation(c1.hue, c2.hue, percent),
            approach(c1.saturation, c2.saturation, percent),
            approach(c1.value, c2.value, percent),
        );
        return nextColor.hex;
    }

    /**
     * interval is just the update frequency
     * @return {Number}
     */
    getInterval() {
        return this.updateFrequency;
    }

    /**
     * To plain object for APi
     * @return {object}
     */
    toPlainObject() {
        const obj = super.toPlainObject();
        obj.steps = this.steps;
        obj.function = this.function;
        obj.clockwise = this.clockwise;
        return obj;
    }
}

export default FadeStrategy;
