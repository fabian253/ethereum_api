USE ethereum_api;

SELECT table_name AS "Table",
ROUND(((data_length + index_length) / 1024 / 1024), 2) AS "Size (MB)"
FROM information_schema.TABLES
WHERE table_schema = "ethereum_api"
ORDER BY (data_length + index_length) DESC;

show databases;

select * from contract where contract_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D";

select * from transaction limit 10;

select count(*) from transaction;

select count(*) from transaction where contract_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D";

select * from transaction where contract_address = "0x1B829B926a14634d36625e60165c0770C09D02b2";

select contract_address, count(*) from transaction group by contract_address;

show tables;

show open tables where in_use>0;

show processlist;

select Count(*) from contract limit 10;

select Count(*) from contract where block_minted is not null;

select * from contract where contract_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D";

select * from contract where contract_address = "0x8821BeE2ba0dF28761AffF119D66390D594CD280";

select ERC20, ERC721, count(*) from contract group by ERC20, ERC721;

select * from contract limit 10;

select * from contract where ERC721 = 1 limit 10000;

SELECT * from contract where ERC20 = 0 and ERC20Metadata = 0 limit 10000;

SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = 'contract';