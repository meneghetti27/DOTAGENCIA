// Sobe as artes do @plagio.zip como JPG na pasta do Drive e apaga os Docs de imagem antigos.
// Como usar: script.google.com > Novo projeto > cola tudo > Executar (autoriza na 1a vez).
function subirArtes() {
  var pasta = DriveApp.getFolderById('1uzYQtxh1DsKad4YvWvojPPZlF6OkF1vd'); // PLAGIO POSTS / Semana 1
  var base = 'https://raw.githubusercontent.com/meneghetti27/DOTAGENCIA/claude/loving-franklin-c8o6kc/plagio/rodada-1/drive-semana-1/';
  var nomes = ['Post 01', 'Post 02', 'Post 03', 'Post 04', 'Post 05', 'Post 06 (postar 09-11)',
               'Post 07', 'Post 08', 'Post 09', 'Post 10'];
  nomes.forEach(function (nome) {
    var blob = UrlFetchApp.fetch(base + encodeURIComponent(nome + '.jpg')).getBlob().setName(nome + '.jpg');
    pasta.createFile(blob);
    var docs = pasta.getFilesByName(nome); // Doc antigo com a imagem dentro
    while (docs.hasNext()) {
      var f = docs.next();
      if (f.getMimeType() === MimeType.GOOGLE_DOCS) f.setTrashed(true);
    }
  });
  Logger.log('Pronto: 10 JPGs na pasta Semana 1.');
}
