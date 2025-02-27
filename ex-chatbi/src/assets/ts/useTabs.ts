import { ref } from 'vue';
import type { TabsPaneContext } from 'element-plus';

export function useTabs() {
  const activeName = ref('first');

  const handleClick = (tab: TabsPaneContext, event: Event) => {
    console.log(tab, event);
  };

  return {
    activeName,
    handleClick,
  };
}