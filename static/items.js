/** 
 * Functions to render the item html
 */
const $pokeballs = $('#pokeballs')
const $healing = $('#healing')
const $battle = $('#battle')
const $other = $('#other')
const baseApi = 'https://pokeapi.co/api/v2'

async function sortItems(results){

    let items = results.data.results
    for (i=0; i<items.length; i++){
        let itemData = await axios.get(`${items[i].url}`)
        if (itemData.data.category.name === "standard-balls" || itemData.data.category.name === "special-balls" || 
        itemData.data.category.name === "apricot-balls"){
            $pokeballs.append(`<li><a href = '/items/${itemData.data.id}'> ${items[i].name}</a></li>`)
        }
        else if (itemData.data.category.name === "healing" || itemData.data.category.name === "status-cures"
        ||itemData.data.category.name === "pp-recovery" || itemData.data.category.name === "revival"){
            $healing.append(`<li><a href = '/items/${itemData.data.id}'>${items[i].name}</li>`)
        }
        else if (itemData.data.category.name === "stat-boosts"){
            $battle.append(`<li><a href = '/items/${itemData.data.id}'>${items[i].name}</li>`)
        }
        else{
            $other.append(`<li><a href = '/items/${itemData.data.id}'>${items[i].name}</li>`)
        }

    }
    
    if (results.data.next !== 'null'){
        nextSet = await axios.get(`${results.data.next}`)
        console.log(results.data.next)
        sortItems(nextSet)
}
}

async function sortHealing(results){

    let items = results.data.results
    for (i=0; i<items.length; i++){
        let itemData = await axios.get(`${items[i].url}`)
        if (itemData.data.category.name === "healing" || itemData.data.category.name === "status-cures"
        ||itemData.data.category.name === "pp-recovery" || itemData.data.category.name === "revival"){
            $healing.append(`<li><a href = '/items/${itemData.data.id}'>${items[i].name}</li>`)
        }
    }
    
    if (results.data.next !== "https://pokeapi.co/api/v2/item?offset=780&limit=20"){
        nextSet = await axios.get(`${results.data.next}`)

        sortHealing(nextSet)
    }
    else {
        data = await axios.get(`${baseApi}/item`)
        sortHealing(data)
    }
}


async function populateItemList(){
    const results = await axios.get(`${baseApi}/item`)

    sortItems(results)
}
document.body.onload=populateItemList()
