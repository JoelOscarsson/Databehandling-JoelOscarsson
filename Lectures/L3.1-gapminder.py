import plotly_express as px
gapminder = px.data.gapminder()

# We want to make dots whose size is scaled to how big the country is
fig = px.scatter(
    gapminder,
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    log_x=True,
    size_max=70,
    color="country",
    animation_frame="year",
    animation_group="country", title="Gapminder",
    range_y = [25, 90], range_x = [100, 100_000]  # Vi vill kapa för att den kommer hoppa mellan axlarna, när man går framåt

)

#fig.show()

fig.write_html("3.1_gapminder.html", auto_open = True)