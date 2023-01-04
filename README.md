# Yu-Gi-Oh! Hand master

A python algorithm for calculating the chances of drawing a sample of cards from a deck.

Included is a method which draws a random sample multiple times and counts if the sample is a success or not
and a method which calculates the probability of a certain sample with the hypergeometric probability/cumulative 
distribution function.

## Installation

Use GIT bash [GIT](https://git-scm.com/downloads) to clone th is repository.

```bash
git clone https://github.com/Konisaurus/YGO_hand_calculation.git
```

## Usage

```python
import hand_simulation
import hypgeo_distribution_function

# The Deck_Controller class needs a deck_dictionary = {"card name": number of copies, ...}
deck = Deck_Controller(deck_dict)

# Create differen card pools in your deck. You can add multiple card pools in one shot. Your card pools can contain multiple cards.
# Furthermore, state how many times a card from a pool should be in a sample, so the sample is a success. 
# True:  success when X == 1
# False: success when X >= 1
deck.create_card_pools([Card_Pool(["card 1", "card 2"], 1, False), Card_Pool(["card 3"], 2, True)])

# Now, you can do some calculations
sample_simulation(deck, iterations, sample_size)
hypgeo_cdf(deck, sample_size)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

No license whatsoever :)
