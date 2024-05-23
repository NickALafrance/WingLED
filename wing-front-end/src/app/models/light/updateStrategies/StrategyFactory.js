import FadeStrategy from './FadeStrategy';
import JumpStrategy from './JumpStrategy';
import NullStrategy from './NullStrategy';

/**
 * Factory to create update strategy.
 * @param {object} config
 * @return {UpdateStrategyInterface}
 */
export default function makeFactory(config) {
    switch (config?.type) {
    case 'Jump':
        return new JumpStrategy(config);
    case 'Fade':
        return new FadeStrategy(config);
    default:
        return new NullStrategy(config);
    }
}
