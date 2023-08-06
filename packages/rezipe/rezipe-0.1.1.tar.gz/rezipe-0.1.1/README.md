# Rezipe 👨‍🍳👩‍🍳🍽
A way to write down your cooking/baking recipes in Python. This is an actual library, no joke (period). Made with ❤ for everyone with minimum coding literacy.

> ⛑ This is under developement.

```python
import pint

from rezipe import Measure, recipe
from rezipe.wares import Pot
from rezipe.ingredients import RegularTofu, SnowPea, EnokiMushroom, DashiSoup, Miso

ureg  = pint.UnitRegistry()

class MisoSoup(Rezipe):
    """
    A simple miso soup by Rie
    """
    ref = "https://tasty.co/recipe/miso-soup"

    # kichenwares
    pot: Pot = Pot()

    # Ingredients
    dashi: DashiSoup = Measure(360 * ureg.mL)
    tofu: RegularTofu = Measure(200 * ureg.gram)
    pea: SnowPea = Measure(75 * ureg.gram)
    mushroom: EnokiMushroom = Measure(55 * ureg.gram)
    miso: Miso = Measure(2*ureg('tablespoon'))

    @recipe
    async def make(self):
        # class variable auto expose from method variable?
        pot += dashi
        await pot.boil()

        # self assign inplace async, is it even possible?
        await tofu.cut(style="cube")

        # method chaining
        await pea.trim().cut(in="half")

        await mushroom.cut(remove="end")

        pot += tofu + pea + mushroom
        await pot.slimmer().for(3*ureg.min)

        assert pot.heat.isOff
        miso = await miso.dissolve(with=pot.soup)
        pot.add(miso)

        await pot.boil(progress=0.75)

        self.serve(pot)
```

## Features
* Accept concurrent async/await - real home cooker do multiple things at once
* Auto Convertion - enable percise measurement by default
* Easy to fork(searchable, copy and modify) - that is the nature of open source.
* Crystal Clear - yep totally logical and very descriptive


## Roadmap
* Autogen printable recipe/VSCode plugins for assisting read/cli
* Works with your smart home/IoT device
* Auto order/pre-order from your nearby market/farmer
* Auto global ingredient subsitution - how to find nashville hot sauce/butter milk in Udon Thani?
* Auto Nutrition
* Add documentaion/test
* Library of localized ingredients - thanks to inheritance of class, not the all white rice is equal, Not all beef are equal,  `class HomMaliRice(WhiteRice):`, `class Wagyu(Beef)`
* Make this for all popular programing languages
* Able to create a opitimal cooking pipeline when do multiple recipes/dishes things at once
* Able to create a opitimal cooking pipeline when do multiple recipes/dishes things at once
* Enable [Bidirection Alias](https://dev.to/circleoncircles/rewrite-link-bidirectional-aliasing-in-python-ekl) for truly world citizen recipe i.e. `dough.bake` == `แป้งโด.อบ` == `面团.烤`

## Style
This will be a modern python lib.