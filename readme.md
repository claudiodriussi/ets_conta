# ets_conta

**ets_conta** is an Italian project. It is a simple accounting system based on Excel files and it is suitable for small No Profit Associations recognized by italian Law.

Follow the italian documentation.

---

**ets_conta** è un programma per la gestione di una contabilità semplice utilizzando fogli Excel.

Il programma è stato pensato per l'utilizzo da parte degli "Enti del Terzo Settore" da cui deriva il nome "ets_conta" e può essere utilizzato da tutti gli enti che hanno un modesto numero di movimenti contabili e che intendono tenere la contabilità con il criterio di cassa. Al di sopra dei 1000 movimenti contabili all'anno riteniamo opportuno pensare ad altre soluzioni.

Il programma è stato sviluppato a partire da un precedente progetto chiamato "lug_conta" che è stato usato con successo per alcuni anni per tenere la contabilità della [APS PNLug](https://www.pnlug.it/). L'intento di questa nuova versione è quello di togliere alcune funzioni ritenute inutili ed aggiungerne altre, ed anche quello di facilitare l'uso da parte di personale inesperto.

Tutto parte da un foglio di calcolo chiamato "Primanota" nel quale vengono inserite le scritture contabili e dal quale vengono generati automaticamente alcuni fogli di calcolo con i dati aggregati in modo contabile.

Per ogni anno contabile viene preparato un nuovo foglio di "Primanota" dedicato ed alcuni altri fogli che contengono alcune liste di dati. Poi un programma dedicato si occupa della generazione dei risultati contabili.

## Installazione

Il programma che genera i risultati contabili richiede Python 3 preferibilmente in un ambiente virtualenv.

Le istruzioni che seguono si riferiscono al sistema operativo Linux, ma per chi ha un minimo di competenze informatiche sarà facile portarle su altri sistemi operativi e realizzare eventuali automatismi.

Si fa così:

Si crea una cartella e si copiano i files del progetto, poi si apre un terminale e si danno questi comandi:

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -U pip
$ pip install -r requirements.txt
```

dalla seconda volta in poi sarà sufficiente scrivere:

```
$ source venv/bin/activate
```

## Utilizzo

Dopo aver fatto l'installazione si possono inserire nel file di Primanota le scritture contabili come spiegato più avanti e quando si desidera si può eseguire il calcolo.

Per fare questo prima si deve avviare l'ambiente virtuale di Python con:

```
$ source venv/bin/activate
```

e poi lanciare il programma comando:

```
$ python conta_gui.py
```
Da cui è possibile scegliere il file da calcolare e quali fogli generare.

Esiste anche una versione a riga di comando:

```
$ python ets_conta.py esempio/PRIMANOTA.xlsx
```
in cui si sostituisce `esempio` con la cartella dei dati dell'anno da ricalcolare.

Il programma in effetti contiene tutte le procedure di calcolo, però può risultare scomodo e solitamente si preferisce l'applicazione grafica.

Il sistema presuppone che nella cartella che contiene il file della primanota sia presente una cartella di nome `dati` che contiene i files con i nomi dei `conti`, degli `eventi` e delle `anagrafiche`. Tutti questi parametri sono configurabili con il file `config.yaml` che deve essere presente nella cartella del programma.

Il risultato sono una serie di files \*.xlsx che per default vengono messi nella cartella `documenti`.

## Struttura dei dati

Le righe del file di primanota sono le seguenti:

**DATA, DESCRIZIONE, CONTO DARE, CONTO AVERE, IMPORTO, EVENTO, TAGS, ANAGRAFICA**

Il conto dare ed il conto avere devono essere entrambi presenti e devono essere presenti anche nel file `CONTI.xlsx` altrimenti il programma andrà in errore. Questo è stato fatto per evitare errori di battitura e l'utilizzo di conti non pianificati.

L'evento è opzionale e si usa quando una determinata operazione viene fatta con riferimento ad un evento o progetto. Il campo tags viene utilizzato per specificare l'evento. Ad esempio l'evento "CORSI" può avere il tag "BASH" oppure "PYTHON1" per separare le scritture relative ai due corsi.

Anche l'anagrafica è opzionale e permette di creare una scheda per ogni soggetto implicato nei dati contabili, ad esempio un socio o un fornitore.

I files `CONTI.xlsx`, `ANAGRAFICHE.xlsx` ed `EVENTI.xlsx` si trovano di solito nella cartella `dati` dentro alla cartella che contiene il file di primanota e sono composti semplicemente dai campi **CODICE e DESCRIZIONE**

Infine il file `config.yaml` in caso di necessità permette di configurare i parametri.

## Inserimento dati

L'inserimento dei dati è molto semplice ed usa la regola contabile della **"Partita doppia"**, in cui ogni operazione monetaria avviene tra due conti.

Per convenzione il conto **DARE** è quello che riceve il denaro ed il conto **AVERE** è quello che da il denaro, ad esempio se un socio paga la quota associativa in dare va la CASSA o la BANCA ed in avere va il conto SOCI. Oppure se si acquistano dei materiali di consumo in dare va il conto ATTREZZATURA ed in dare il conto CASSA

Per convenzione i movimenti in dare hanno segno positivo ed i movimenti in avere hanno segno negativo, ma questo viene gestito automaticamente. Se serve (ad esempio per scritture di rettifica) si possono inserire importi negativi, ed in tal caso i segni verranno invertiti.

Non è necessario inserire i dati ordinati per data, ma è preferibile.

Non è necessario generare i files automatici tutte le volte che si inseriscono dati, ma solo quando serve avere dei consuntivi.

È preferibile fare un file di primanota per ciascun anno.

## Files generati

I files generati dal programma sono:

* **BILANCIO** fa la somma di tutti i movimenti di ciascun conto e riporta il totale.
* **SCHEDE** per ciascun conto vengono generate le schede contabili che contengono la lista dei movimenti ed il saldo.
* **EVENTI** per ciascun evento vengono riportate i movimenti di spesa o di ricavo in modo da avere il saldo economico. I movimenti vengono ordinati per tag e per data, in questo modo si possono fare i subtotali per ciascun tag.
* **ANAGRAFICHE** per le scritture che contengono l'indicazione dell'anagrafica vengono riportati i movimenti di spesa e di ricavo in modo da avere il saldo economico.
* **GIORNALE** è molto simile alla primanota, con la sola differenza che c'è una riga per ciascun conto e che in caso di necessità le righe vengono riordinate per data.

## Limiti

Il sistema fa uso di fogli `Excel versione 2007 - 365` perché vengono gestiti in modo ottimo dalle librerie di Python, ma ne fa un utilizzo assolutamente basico escludendo tutte le funzionalità avanzate di Excel. Questa è stata una scelta progettuale atta a mantenere semplici i files di dati.

Il sistema risulta pratico e comodo quando il numero delle registrazioni contabili ed il numero dei dati anagrafici per ogni anno non è molto elevato, dal punto di vista del programma non conosco i limiti operativi, ma ritengo che anche in presenza di molte migliaia di righe il funzionamento sia ottimale, ma dal punto di vista pratico se i movimenti ed i riferimenti anagrafici sono tanti probabilmente conviene pensare ad una soluzione più strutturata e controllata.

In caso di errori nella configurazione o nel formato dei files, viene segnalato l'errore a livello di linguaggio, invece se l'errore è nella digitazione dei conti o degli eventi o anagrafiche, l'errore indica il nome che non è stato trovato.

## Dettagli funzionali e normativi

Per i dettagli normativi invitiamo a consultare la documentazione normativa facilmente reperibile su internet, di seguito riportiamo alcuni criteri operativi.

Il regolamento del Terzo Settore indica che al di sotto di un certo importo la contabilità può essere tenuta utilizzando ***il criterio di cassa***.

Il ***il criterio di cassa*** è un regime contabile semplificato in cui non è richiesta la gestione dello stato patrimoniale e quindi dei beni durevoli posseduti dall'ente. È sufficiente registrare le entrate e le uscite realizzate tramite contante o tramite mezzi bancari e specificare il motivo della transazione.

Nel nostro caso abbiamo ritenuto utile aggiungere le funzionalità di **Evento** e **Anagrafica** che eseguono raggruppamenti specifici per questi parametri. Questa gestione non è strettamente necessaria ma è utile per per rendicontare eventi o progetti. Tecnicamente questa gestione si chiama **"Contabilità analitica"**

Di solito gli enti non sono soggetti obbligati IVA, ma possiedono solo il Codice Fiscale, questo significa che non sono tenuti agli obblighi di fatturazione elettronica e per contro la componente IVA risulta essere un costo.

La recente normativa prevede che gli Enti del Terzo Settore siano iscritto al ***RUNTS*** *(Registro unico nazionale del Terzo Settore)*. Per ottenere l'iscrizione è necessario che lo statuto venga redatto secondo criteri stabiliti, sono anche previsti obblighi assicurativi ed è necessario che i dati di bilancio vengano inviati in modo telematico e siglati con la Firma Digitale.

Per la contabilità con ***criterio di cassa*** è stato reso disponibile un foglio Excel di esempio che potrà essere compilato con i dati provenienti dal bilancio da noi generato. Alleghiamo a questo progetto un esempio di file ed alcune annotazioni su come compilarlo.

## Donazioni ed assistenza.

Se utilizzate questo programma potete fare una donazione con paypal

[![paypal](https://www.paypalobjects.com/it_IT/IT/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate/?hosted_button_id=2BYE4T9EEALQ6)

Se vi serve aiuto per installare il programma, o vi serve spiegazioni o modifiche mi potete contattare via mail all indirizzo: claudio.driussi@gmail.com
