% Definir os dynamic para cada um dos predicados
:-dynamic (utente/4).
:-dynamic (ato/8).
:-dynamic (marcador/6).
:- op(900, xfy, '::').
:- dynamic ('-'/1).
:- op(900, xfy, 'e').
:- op(900, xfy, 'ou').

% ------------------------------------------------------------------------------------------- 
% -------------------------------- Informacao Dada ------------------------------------------ 
% -------------------------------------------------------------------------------------------

% utente: #IdUt, Nome do utente, Data de Nascimento, Sexo -> { V,F,D }
% ato: #IdAto, Data, #IdUt, Idade, Colesterol, Pulsacao, Pressao -> { V,F,D }
% marcador: #IdMarcador, Analise, Idade, Sexo, Minimo, Maximo -> { V,F,D }

% ------------------------------------------------------------------------------------------- 
% ---------------------------- Conhecimento Positivo ---------------------------------------- 
% -------------------------------------------------------------------------------------------

% Extensao do predicado utente:  IdUt, Nome, (Dia, Mes, Ano), Sexo -> { V,F,D }

utente(123456780, antonio, (30,06,1990), masculino).
utente(987654321, beatriz, (30,07,1985), feminino).
utente(135246978, carlos, (30,08,1987), masculino).

utente(111133333, raquel, (14,10,2002), feminino).
utente(222223333, sofia, (3,07,1989), feminino).
utente(333334444, helena, (4,02,1990), feminino).
utente(444445555, marta, (15,03, 1995), feminino).
utente(555556666, diana, (13,04,2000), feminino).
utente(666667777, joana, (21,12,1988), feminino).


% Extensao do predicado ato: IdAto, (Dia, Mes, Ano), IdUt, Idade, Colesterol, Pulsacao, PInf, PSup -> { V,F,D }

ato(gmr02067, (30,06,2020), 123456780, 30, 140, 70, 60, 123).
ato(gmr2183, (30,07,2021), 987654321, 36, 190, 60, 70, 142).
ato(gmr2297, (30,06,2022), 123456780, 32, 230, 90, 65, 151).

ato(gmr1111, (12,9,2020), 111133333, 18, 260, 90, 50, 80).
ato(gmr22223, (01,01,2019), 222223333, 30, 160, 170, 200, 80).
ato(gmr22223, (02,03,2018), 333334444, 28, 140, 120, 80, 310).


% Extensao do predicado marcador:  IdMarcador, Analise, Idade, Sexo, VMinimo, VMaximo -> { V,F,D }

marcador(ctm01, colesterol, (18,30), masculino, 0, 170).
marcador(ctf02, colesterol, (18,30), feminino, 0, 160).
marcador(ctm03, colesterol, (31,45), masculino, 0, 190).
marcador(ctf04, colesterol, (31,45), feminino, 0, 180).
marcador(psm05, pulsacao, (18, 25), masculino, 60, 80).



% ------------------------------------------------------------------------------------------- 
% ---------------------------- Conhecimento Negativo ---------------------------------------- 
% -------------------------------------------------------------------------------------------

% O utente de id 1928238723, julio  e a utente carolina de id 9999888777  ja nao estao inscritos no centro de saude/clinica  
-utente(1928238723, julio, (22,04,1990), masculino).
-utente(9999888777, carolina, (12,04,2001), feminino).

% a clinica nao faz analises do marcador Glicose, hormonaX, ureia   

-marcador(gl01, glicose, (18,45), feminino, 40, 100).
-marcador(hr02, hormonaX, (18,45), feminino, 30, 60).


% a clinica nao tem marcadores para menores de 18 
-marcador(ctm03, colesterol, (0,18), masculino, 0, 170).
-marcador(ctf03, colesterol, (0,18), feminino, 0, 170).



% ------------------------------------------------------------------------------------------- 
% --------------------------------- Evolucao da BC ------------------------------------------ 
% -------------------------------------------------------------------------------------------  

% Extensao do predicado que permite a evolucao do conhecimento

evolucao(Termo) :-
    findall(Invariante, +Termo::Invariante, Lista),  
    insercao(Termo),
    teste(Lista).

insercao(Termo) :-assertz(Termo).
insercao(Termo) :-retract(Termo),!, fail.

teste([]).
teste([R|LR]):- R, teste(LR).



% ------------------------------------------------------------------------------------------- 
% ------------------------------ Invariantes de Insercao ------------------------------------ 
% ------------------------------------------------------------------------------------------- 

% Invariante Estrutural:  nao permitir a insercao de conhecimento repetido

% Nao permitir a insercao de Utentes com igual IdUtente e Nome !funciona
+utente(IdUt, Nome , (Dia, Mes, Ano), Sexo) :: (findall((IdUt, Nome),(utente( IdUt, Nome , (Dia, Mes, Ano), Sexo)), S),
                  comprimento( S,N ), 
				  N == 1 ).

% Nao permitir a insercao de Utentes com igual IdUtente !funciona
+utente(IdUt, _ , _, _) :: (findall((IdUt),(utente(IdUt, _ , _, _)), S),
                  comprimento( S,N ), 
				  N == 1 ).

% Nao permitir a insercao do mesmo ato, ou seja, a insercao de Ids iguais !funciona
+ato(IdAto, _, _, _, _, _, _, _) :: (findall((IdAto), (ato(IdAto, _, _, _, _, _, _, _)), S),
                  comprimento(S,N),
                  N==1).

% Nao permitir a insercao de ato relacionado a um utente que nao existe !funciona
+ato(_, _, IdUt, _, _, _, _, _) :: (findall((IdUt),((ato(_, _, IdUt, _, _, _, _, _)), (utente(IdUt,_, _, _))), S),
                  comprimento(S,N),
                  N>=1).                  
				  
% nao permitir a insercao de utentes com mais de 45 anos (porque assumimos que nao temos marcadores para essa idade) !funciona
+utente(_, _,(_,_,A), _) :: (findall((A),
                                (utente(_,_,(_,_,A), _), A<1977), 
                                L),
                                comprimento(L,N),
                                N==0).

% nao permitir a insercao de utentes com menos de 18 anos (porque assumimos que nao temos marcadores para essa idade) !funciona


+utente(_, _,(_,_,A), _) :: (findall((A),(utente(_, _,(_,_,A), _), A>2004), L),
                             comprimento(L,N),
                             N==0).

% nao inserir  ato q a pulsacao esta a 0 (se nao a pessoa estaria morta) ->  funciona
+ato(_, _, _, _, _, Pul, _, _) :: (findall((Pul),(ato(_, _, _, _, _, Pul, _, _), Pul=<0), L),
                                    comprimento(L,N),
                                    N==0).

% nao permitir ato q colesterol esta a 600, fora dos valores considerados possiveis  ->  funciona
+ato(_, _, _, _, Col, _, _, _) :: (findall((Col),
                                (ato(_, _, _, _, Col, _, _, _), Col>600), 
                                L), 
                                comprimento(L,N),
                                N==0).

% invariante para nao inserir conheciemtno negativo de um utente quando ha conhecimento perfeito positivo para esse utente
+(-utente(IdUt, Nome , (Dia, Mes, Ano), Sexo)):: (findall((IdUt),(utente(IdUt, Nome , (Dia, Mes, Ano), Sexo)),L), 
                                            comprimento(L,N), N==0).

% invariante para nao inserir um utente quando ha conhecimento perfeito negativo para esse utente
+utente(IdUt, Nome , (Dia, Mes, Ano), Sexo):: (findall((IdUt),(-utente(IdUt, Nome , (Dia, Mes, Ano), Sexo)),L), 
                                            comprimento(L,N), N==0).


% ------------------------------------------------------------------------------------------- 
% --------------------------------- Involucao da BC -----------------------------------------
% ------------------------------------------------------------------------------------------- 

% Extensao do predicado que permite a involucao do conhecimento

involucao( Termo ) :-
    findall(Invariante, -Termo::Invariante, Lista),
    remocao(Termo),
    teste(Lista).

remocao(Termo):-retract(Termo).
remocao(Termo):-assertz(Termo), !, fail.

teste([]).
teste([R|LR]):-R,teste(LR).

% ------------------------------------------------------------------------------------------- 
% ------------------------------ Invariantes de Remocao ------------------------------------- 
% ------------------------------------------------------------------------------------------- 


% Nao remover o utente se tiver um ato associado !FUNCIONA!
-utente(IdUt,_,_,_)::(findall((IdUt),(ato(_,_,IdUt,_,_,_,_,_)), S),
                   comprimento( S,N ), 
				   N == 0 ).

% nao remover o marcador se a existirem atos com idade dentro do marcador
-marcador(IdMarc, Nome, (IMin, IMax), Sexo,Vmin, Vmax)::(findall((Idade), (ato(IdAto, (DataN), IdUt, Idade, Col, Pul, PInf, PSup), Idade<IMax, Idade>IMin), L),
                                                        comprimento(L,N),
                                                        N==0).



% ------------------------------------------------------------------------------------------- 
% ------------------------------ Sistemas de Inferencia ------------------------------------- 
% ------------------------------------------------------------------------------------------- 
% Extensao do meta-predicado si: Questao,Resposta -> {V,F,D}

si(Questao, verdadeiro) :-
    Questao.
si(Questao, falso) :-
    -Questao.
si(Questao, desconhecido) :-
    nao(Questao),
    nao(-Questao).

% si conjuncao e disjuncao 

% Extensao do meta-predicado siL: [],[] -> {V,F,D}

siL([],[]).
siL([Questao|L],[Resposta|S]):-
	siL(L,S),
    si(Questao,Resposta).


% Extensao do meta-predicado siC: Questao1 e Questao2, Resposta -> {V,F,D}

siC(Q1 e Q2, verdadeiro) :- 
	si(Q1, verdadeiro), 
	si(Q2, verdadeiro).
siC(Q1 e Q2, falso) :- 
	si(Q1, verdadeiro), 
	si(Q2, falso).
siC(Q1 e Q2, desconhecido) :- 
	si(Q1, verdadeiro), 
	si(Q2, desconhecido).
siC(Q1 e Q2, falso) :- 
	si(Q1, falso), 
	si(Q2, verdadeiro).
siC(Q1 e Q2, falso) :-
	si(Q1, falso),
	si(Q2, falso).
siC(Q1 e Q2, falso) :-
	si(Q1, falso),
	si(Q2, desconhecido).
siC( Q1 e Q2, desconhecido) :-
	si(Q1, desconhecido),
	si(Q2, verdadeiro).
siC(Q1 e Q2, falso) :-
	si(Q1, desconhecido),
	si(Q2, falso).
siC(Q1 e Q2, desconhecido) :-
	si(Q1, desconhecido),
	si(Q2, desconhecido).

% Extensao do meta-predicado siD: Questao1 ou Questao2, Resposta -> {V,F,D}
siD(Q1 ou Q2, verdadeiro) :-
	si(Q1, verdadeiro),
	si(Q2, verdadeiro).
siD(Q1 ou Q2, verdadeiro) :-
	si(Q1, verdadeiro),
	si(Q2, falso).
siD(Q1 ou Q2, verdadeiro) :-
	si(Q1, verdadeiro),
    si(Q2, desconhecido).
siD(Q1 ou Q2, verdadeiro) :-
	si(Q1, falso),
	si(Q2, verdadeiro).
siD(Q1 ou Q2, falso) :-
	si(Q1, falso),
	si(Q2, falso).
siD(Q1 ou Q2, desconhecido) :-
	si(Q1, falso),
	si(Q2, desconhecido).
siD(Q1 ou Q2, verdadeiro) :-
	si(Q1, desconhecido),
	si(Q2, verdadeiro).
siD(Q1 ou Q2, desconhecido) :-
	si(Q1, desconhecido),
	si(Q2, falso).
siD(Q1 ou Q2, desconhecido) :-
	si(Q1, desconhecido),
	si(Q2, desconhecido).

% ------------------------------------------------------------------------------------------- 
% ------------------------------ Negacao por Falha ------------------------------------------ 
% ------------------------------------------------------------------------------------------- 
% Extensao do meta-predicado nao: Questao -> {V,F}
nao(Questao) :-
    Questao, !, fail.
nao(Questao).

% ------------------------------------------------------------------------------------------- 
% ------------------------- Pressuposto Mundo Fechado --------------------------------------- 
% ------------------------------------------------------------------------------------------- 

-utente(IdUt, Nome , DataN, Sexo):-nao(utente(IdUt,Nome,DataN,Sexo)),
								 nao(excecao(utente(IdUt, Nome , DataN, Sexo))).

-ato(IdAto, Data, IdUt, Idade, Colesterol, Pulsacao, PInf, PSup):-nao(ato(IdAto, Data, IdUt, Idade, Colesterol, Pulsacao, PInf, PSup)),
																  nao(excecao(ato(IdAto, Data, IdUt, Idade, Colesterol, Pulsacao, PInf, PSup))).

-marcador(IdMarcador, Analise, Idade, Sexo, Minimo, Maximo):- nao(marcador(IdMarcador, Analise, Idade, Sexo, Minimo, Maximo)),
                                                              nao(excecao(marcador(IdMarcador, Analise, Idade, Sexo, Minimo, Maximo))).
                                                              

% ------------------------------------------------------------------------------------------- 
% ------------------------------ Predicados Auxiliares -------------------------------------- 
% ------------------------------------------------------------------------------------------- 

% Extensao do predicado comprimento: L, N -> {V,F}
comprimento([],0).
comprimento( L,N ) :-
    length( L,N ).

% predicado para concatenar listas

concatenar([],L,L).
concatenar([X|L1],L2,[X|L3]) :-
    concatenar(L1,L2,L3).    

% predicado para listar o conhecimento positivo relativamente aos utentes

listingutente(L):- findall((utente(IdUt, Nome , (Dia, Mes, Ano), Sexo)),(utente(IdUt, Nome , (Dia, Mes, Ano), Sexo)),L).

% predicado para listar o conhecimento negativo relativo aos utentes

listingnaoutente(L):- findall((utente(IdUt, Nome , (Dia, Mes, Ano), Sexo)),(-utente(IdUt, Nome , (Dia, Mes, Ano), Sexo)),L).

% predicado para listar o conhecimento imperfeito relativo aos utentes	

listingexcecaoutente(L):- findall((utente(IdUt, Nome , (Dia, Mes, Ano), Sexo)),(excecao(utente(IdUt, Nome , (Dia, Mes, Ano), Sexo))),L).

% predicado para listar o conhecimento positivo, negativo e desconhecido relativo aos utentes.

listingtodosutentes(L):-listingutente(L1), listingnaoutente(L2), listingexcecaoutente(L3), concatenar(L1,L2, Ltemp), concatenar(Ltemp, L3, L).


% ------------------------------------------------------------------------------------------- 
% ------------------------- Conhecimento imperfeito incerto --------------------------------- 
% ------------------------------------------------------------------------------------------- 

% O utente de id 111222333 e de nome Silvio chega ao centro de saude visivelmete perturbado e nao sabe a sua data de nascimento. 

utente(111222333, silvio, xpto1, masculino). 
excecao(utente(IdUt,Nome,(Dia, Mes, Ano),Sexo)):-utente(IdUt,Nome,xpto1,Sexo).


% Ocorreu uma falha nas analises e nao foi possivel determinar o valor de colesterol do ato de id gmr02000. 

ato(gmr02000, (18,11,2022), 4545456666, 30, xpto2, 70, 60, 123).
excecao(ato( IdAto, Data, IdUt, Idade, Colesterol, Pulsacao, PInf, PSup)):- ato(IdAto, Data, IdUt, Idade, xpto2, Pulsacao, PInf, PSup).



% ------------------------------------------------------------------------------------------- 
% ------------------------- Conhecimento imperfeito impreciso ------------------------------- 
% -------------------------------------------------------------------------------------------

% Um utente com id 111222444 com demencia, de sexo masculino e nascido a 13-01-1988 entra de urgencia para fazer analises, mas nao sabe se se chama Raul ou Renato.

excecao(utente(111222444,raul,(13,01,1988),masculino)).
excecao(utente(111222444,renato,(13,01,1988),masculino)).

% Outro utente com id 222333444 de nome Lucia, de sexo feminino sabe que nasceu em 12/1990 mas nao ao certo o dia, sabe apenas que foi na semana do natal, entre 23 a 27.


excecao(utente(222333444,lucia,(23,12,1990),feminino)). 
excecao(utente(222333444,lucia,(24,12,1990),feminino)).  
excecao(utente(222333444,lucia,(25,12,1990),feminino)). 
excecao(utente(222333444,lucia,(26,12,1990),feminino)). 
excecao(utente(222333444,lucia,(27,12,1990),feminino)).                                        


% O ato registado do utente 444555666 na data 23-05-2022 apresenta todos os dados corretos a excecao do parametro Pulsacao, pois ocorreu um erro na medicao e nao se sabe se o valor correto e 60 ou 62.

excecao(ato(gmr02001,(23,05,2022),444555666,35,160,60,61,122)).
excecao(ato(gmr02001,(23,05,2022),444555666,35,160,62,61,122)).



% ------------------------------------------------------------------------------------------- 
% ------------------------- Conhecimento imperfeito interdito ------------------------------- 
% -------------------------------------------------------------------------------------------

% O utente nega-se a revelar o seu sexo, ou seja, esse parametro encontra-se bloqueado e nunca vamos saber.

utente(555666777,gabriel,(17,02,2000), xpto3).
excecao(utente(IdUt, Nome , DataN, Sexo)):- utente(IdUt, Nome , DataN, xpto3).
interdito(xpto3).

% criar uma invariante para garantir que nunca se inseria um sexo neste parametro

+utente(IdUt, Nome , DataN, Sexo)::(findall((Sexo),
                                    (utente(555666777,gabriel,(17,02,2000),Sexo),nao(interdito(Sexo))),
                                    S),
                                    comprimento(S,N),
                                    N==0).

% ------------------------------------------------------------------------------------------- 
% ------------------------- Predicados para relatar analises --------------------------------
% -------------------------------------------------------------------------------------------

% Extensao do predicado para relatar atos do utente
relatar_atos_utente(utente(IdUt, Nome, Data, Sexo), L):- findall(((ato(IdAto, DataAto, IdUt ,Idade,Col,Pul,PInf,PSup))), (ato(IdAto, DataAto, IdUt ,Idade,Col,Pul,PInf,PSup)), L).

% Extensao do predicado para relatar os exames de colesetrol do utente
listagemcolesterol(utente(IdUt, Nome, Data, Sexo), L):-findall((DataAto, Col), (ato(IdAto, DataAto, IdUt ,Idade,Col,Pul,PInf,PSup)), L).

% Extensao do predicado para relatar o historial dos valores de pulsacao do utente
listagempulsacao(utente(IdUt, Nome, Data, Sexo), L):-findall((DataAto, Pul), (ato(IdAto, DataAto, IdUt ,Idade,Col,Pul,PInf,PSup)), L).

% Extensao do predicado para relatar o historial dos valores de pressao do utente
listagempressao(utente(IdUt, Nome, Data, Sexo), L):-findall((DataAto, (PInf,PSup)), (ato(IdAto, DataAto, IdUt ,Idade,Col,Pul,PInf,PSup)), L).

% ------------------------------------------------------------------------------------------- 
% ------------------------- Predicados para analisar valores --------------------------------
% -------------------------------------------------------------------------------------------


% Extensao do predicado dentropulsacao que devolve uma lista dos utentes que se adequam ao maracadorpulsacao2								
dentropulsacao(L):- findall((IdUt,Nome,DataA,Pul), 
                                ((ato(_, DataA,IdUt,Idade,_,Pul,_,_)),Pul>=60,Pul=<80, Idade=<45, Idade>=30,
                                (utente(IdUt, Nome, Data, masculino))), 
                                L).

                                
% Extensao do predicado forapulsacao que devolve uma lista dos utentes que nao se adequam ao maracadorpulsacao2
forapulsacao(L):- findall((IdUt,Nome,DataA,Pul), 
                               ((ato(_, DataA,IdUt,Idade,_,Pul,_,_)),(Pul<60;Pul>80), Idade=<45, Idade>=30,
                                (utente(IdUt, Nome, Data, masculino))), 
                                L).	



% ------------------------------------------------------------------------------------------- 
% ------------------------- Predicados para alterar informacao ------------------------------
% -------------------------------------------------------------------------------------------

% Extensao do predicado alterar sexo do registo utente
alterar_sexo(IdUt,Nome, Sexo):- involucao(utente(IdUt, Nome ,(Dia, Mes, Ano), _ )),
						evolucao(utente(IdUt, Nome , (Dia, Mes, Ano), Sexo)).

% Extensao do predicado alterar_data_ato 
alterar_data_ato(IdAto, (Dia, Mes, Ano)):- involucao(ato(IdAto,_, IdUt,Idade, Colesterol, Pulsacao, PInf, PSup)), 
						  evolucao(ato(IdAto,(Dia, Mes, Ano), IdUt,Idade, Colesterol, Pulsacao, PInf, PSup)).
		
% Extensao do predicado alterar_data_ato        
alterar_nome_utente(IdUt,Nome):- involucao(utente(IdUt,_, (Dia, Mes, Ano),Sexo)),
						evolucao(utente(IdUt, Nome , (Dia, Mes, Ano), Sexo)).


% predicado para alterar um utente que nao existe para conheciemtno q esse utente existe (conhecimento negativo para positivo)

alterarnaoutente(-utente(IdUt, Nome , (Dia, Mes, Ano), Sexo)):- involucao(-utente(IdUt, Nome , (Dia, Mes, Ano), Sexo)),
                                                                evolucao(utente(IdUt, Nome , (Dia, Mes, Ano), Sexo)).

% predicado para alterar um utente para  utente que nao existe (conhecimento positivo para negativo)
alterarutente(utente(IdUt, Nome , (Dia, Mes, Ano), Sexo)):- involucao(utente(IdUt, Nome , (Dia, Mes, Ano), Sexo)),
                                                                evolucao(-utente(IdUt, Nome , (Dia, Mes, Ano), Sexo)).
                                                                

