/* global jQuery */

const WaitBox = {
    show: () => {
        // TODO
    },
    hide: () => {
        // TODO
    }
};

class Card {
    constructor(idx, num, cattle) {
        this.idx = idx;
        this.num = num;
        this.cattle = cattle;
    }

    toDiv() {
        const toSkull = () => '<img src="/static/skull-solid.svg">';
        const skulls = Array.from({ length: this.cattle }, toSkull).join('');
        return `<div class="card" data-idx="${this.idx}"><div class="skulls top">${skulls}</div><div class="num">${this.num}</div><div class="skulls bottom">${skulls}</div></div>`;
    }
}

class Deck {

    update(cards) {
        this.cards = cards;
    }

    display(postAction) {
        const selector = '.player-deck';
        const container = document.querySelector(selector);
        container.innerHTML = '';
        this.cards.forEach(card => {
            container.insertAdjacentHTML('beforeend', card.toDiv());
        });
        container.querySelectorAll('.card').forEach(el => {
            el.addEventListener('click', (ev) => {
                WaitBox.show();
                const idx = ev.target.dataset.idx;
                postAction(idx);
            });
        });
    }
}

class Table {
    constructor() {
        this.rows = [];
    }

    update(rows) {
        this.rows = rows;
    }

    display() {
        const selector = '.table';
        const container = document.querySelector(selector);

        this.rows.forEach(row => {
            const cards = row.map(card => card.toDiv()).join('');
            const div = `<div class="row">${cards}</div>`;
            container.insertAdjacentHTML('beforeend', div);
        });
    }
}

const NUM = 0;
const CATTLE = 1;

class Game {

    constructor() {
        this.table = new Table();
        this.deck = new Deck();
    }

    start() {
        this.postMove(-1);
    }

    display(data) {
        const toRow = obj => Array.from(obj, toCard).filter(nonZero);
        const toCard = (obj, idx) => new Card(idx, obj[NUM], obj[CATTLE]);
        const nonZero = card => card.num > 0;

        const tableRows = data.piles.map(toRow);
        this.table.update(tableRows);

        const handCards = Array.from(data.hand_cards, toCard).filter(nonZero);
        this.deck.update(handCards);

        const points = Object.entries(data.player_dict).map(player => {
            const name = player[0];
            const sum = player[1].penalty_sum;
            return { name: name, sum: sum };
        });
        this.displayPoints(points);

        this.table.display();
        this.deck.display(idx => this.postMove(idx));
    }

    displayPoints(players) {
        const container = document.querySelector('.points');
        container.innerHTML = '';
        players.forEach(p => {
            const html = `<div class="entry"><div>${p.name}</div><div class="sum">${p.sum}</div></div>`;
            container.insertAdjacentHTML('beforeend', html);
        });
    }

    postMove(idx) {
        const obj = { "action": idx };
        jQuery.ajax('make_action', {
            data: JSON.stringify(obj),
            contentType: 'application/json',
            type: 'POST',
        }).done(data => {
            console.log(data);
            this.display(data);
        });
    }
}

const G = new Game();
window.addEventListener('DOMContentLoaded', () => G.start());
