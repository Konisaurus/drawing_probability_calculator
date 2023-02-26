# Drawing Probability Master

A python algorithm for calculating the chance of drawing a sample of cards from a deck.

It includes the following features:
- A GUI for setting up a desired sample hand.
- Importing/storing decks.
- Calculating the probability of a certain sample with the hypergeometric cumulative distribution
  function.

## Installation

Use GIT bash [GIT](https://git-scm.com/downloads) to clone th is repository.

```bash
git clone https://github.com/Konisaurus/drawing_probability_calculator.git
```

## Usage

Start the program by running the main.py file.

The following files can be imported as a deck:
- .json

```python
  # Here is an example for formatting the .json file.
  {
    "deck name":{
      "card A": number of copies,   # type(number of copies) = int
      "card B": number of copies,
      "card C": number of copies,
      } 
  }
```
- .ydk

  It's a file for storing a Yu-Gi-Oh! deck. This file type is used by multiple
  online simulators that use the [API of YGOPRODeck](https://ygoprodeck.com/api-guide/).
  The card "id"s of the ydk_card_database.json are the same as in the API.

## Contributing

Pull requests are welcome. 
For major changes, please open an issue first to discuss what you would like to change.

## License

No license.
