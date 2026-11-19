// Público: horários e textos que o site mostra.
const { lerAgenda, json } = require('./_lib');
module.exports = async (req, res) => {
  try { json(res, 200, await lerAgenda()); }
  catch (e) { json(res, 500, { erro: 'Não foi possível carregar a agenda.' }); }
};
