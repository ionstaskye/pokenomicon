/**
 * Adds functionality to get more data for abilities
 */

const $ability = $("#ability")
const pokemonList = document.getElementById('ability')
const baseApi = 'https://pokeapi.co/api/v2'

async function makeAbilityList(){
    const $ability = $("#ability")
    const pokemonID = pokemonList.className
    console.log(pokemonID)
    const pokemon = await axios.get(`${baseApi}/pokemon/${pokemonID}`)

    for (i=0; i<pokemon.data.abilities.length; i++){
        const abilityURL = pokemon.data.abilities[i].ability.url
        if (pokemon.data.abilities[i].is_hidden === true){
               const ability = await axios.get(abilityURL)
               $ability.append(`<li>${ability.data.name}(hidden):  ${ability.data.effect_entries[1].short_effect }`)

    }
        else{
            const ability = await axios.get(abilityURL)
            $ability.append(`<li>${ability.data.name}:   ${ability.data.effect_entries[1].short_effect }`)

        }
}
}
document.body.onload = makeAbilityList()