### No more if else code
- 示例一
```python

from NoIf import handle_base


@handle_base.register('strategy_test')
def strategy_1():
    print('strategy_1')


@handle_base.register('strategy_test')
def strategy_2():
    print('strategy_2')

if __name__ == '__main__':
    strategy = handle_base.invoke('strategy_test', 'strategy_1')
    strategy()
```
---
- 示例二
```python
from NoIf import handle_base


class Strategy(object):
    pass


@handle_base.register(Strategy)
class Strategy1(Strategy):

    def test(self):
        print('strategy_1')


@handle_base.register(Strategy)
class Strategy2(Strategy):

    def test(self):
        print('strategy_2')


if __name__ == '__main__':
    strategy_handle = handle_base.invoke(Strategy, 'Strategy1')
    handle = strategy_handle()
    handle.test()
```