/* global jQuery, NAMES */

const WaitBox = {
    show: () => {
        document.body.insertAdjacentHTML('beforeend', `<div class="waitbox"></div>`);
    },
    hide: () => {
        const el = document.querySelector('.waitbox');
        if (el != null) el.remove();
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
        return `
            <div class="card" data-idx="${this.idx}">
                <div class="skulls top">${skulls}</div>
                <div class="num">${this.num}</div>
            </div>`;
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
        container.innerHTML = '';

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
        this.randomizeNames();
        this.postMove(-1);
    }

    randomizeNames() {
        const shuffle = array => {
            for (let i = array.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [array[i], array[j]] = [array[j], array[i]];
            }
        };

        shuffle(NAMES);
        this.names = NAMES.slice(10);
    }

    display(data) {
        const toRow = obj => Array.from(obj, toCard).filter(nonZero);
        const toCard = (obj, idx) => new Card(idx, obj[NUM], obj[CATTLE]);
        const nonZero = card => card.num > 0;

        const tableRows = data.piles.map(toRow);
        this.table.update(tableRows);

        const handCards = Array.from(data.hand_cards, toCard).filter(nonZero);
        this.deck.update(handCards);

        const getName = player => {
            const id = player[0].match(/\d+/)[0];
            if (id > 1) return this.names[id];
            else if (id == 0) return 'AI';
            else if (id == 1) return 'YOU';
            else return 'ERROR';
        };

        const scores = Object.entries(data.player_dict).map(player => {
            const name = getName(player);
            const sum = player[1].penalty_sum;
            return { name: name, sum: sum };
        });
        this.displayScores(scores);

        this.table.display();
        this.deck.display(idx => this.postMove(idx));

        if (handCards.length == 0) data.done = true;

        if (data.done) {
            this.showEndScreen(scores);
        }
    }

    showEndScreen(playerScores) {
        WaitBox.show();

        const byScore = (p1, p2) => p1.sum < p2.sum;
        playerScores.sort(byScore);

        const inner = playerScores.map(score => {
            return `
                <div class="score-row">
                    <div class="player-name">${score.name}</div>
                    <div class="player-sum">${score.sum}</div>
                </div>`;
        }).join('');

        const container = `
            <div class="end-screen">
                ${inner}
                <br /><div class="button play-again">Play again</div>
            </div>`;
        document.body.insertAdjacentHTML('beforeend', container);

        const el = document.querySelector('.play-again');
        el.addEventListener('click', () => {
            const dialog = document.querySelector('.end-screen');
            if (dialog != null) dialog.remove();
            this.start();
        });
    }

    displayScores(playerScores) {
        const container = document.querySelector('.points');
        container.innerHTML = '';
        playerScores.forEach(p => {
            p.sum *= -1;
            const html = `
                <div class="entry ${p.name}">
                    <div>${p.name}</div>
                    <div class="sum">${p.sum}</div>
                </div>`;
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
            this.display(data);
            WaitBox.hide();
        });
    }
}

const G = new Game();
window.addEventListener('DOMContentLoaded', () => G.start());
