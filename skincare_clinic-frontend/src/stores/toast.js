import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useToastStore = defineStore('toast', () => {
    const ms = ref(0);
    const message = ref('');
    const classes = ref('');
    const isVisible = ref(false);

    function showToast(duration, newMessage, newClasses) {
        ms.value = parseInt(duration) || 3000; // fallback to 3s if invalid
        message.value = newMessage || '';
        classes.value = newClasses || '';
        isVisible.value = true;

        setTimeout(() => {
            classes.value += ' -translate-y-28';
        }, 10);

        setTimeout(() => {
            if (typeof classes.value === 'string') {
                classes.value = classes.value.replace('-translate-y-28', '');
            }
        }, ms.value - 500);

        setTimeout(() => {
            isVisible.value = false;
        }, ms.value);
    }

    return {
        ms,
        message,
        classes,
        isVisible,
        showToast,
    };
});
