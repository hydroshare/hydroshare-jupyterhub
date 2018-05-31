#!/usr/bin/env bats

source '/tmp/bats-support/load.bash'
source '/tmp/bats-assert/load.bash'
source '/tmp/bats-file/load.bash'


run-modflow() {
  run mf6.0.2 *.nam
  assert_output --partial 'Normal termination of simulation'
}

# Basic grid analysis
@test "ex01" {
cd ex01-twri
run-modflow
}

@test "ex02" {
cd ex02-tidal
run-modflow
}

@test "ex03" {
cd ex03-bcf2ss
run-modflow
}

@test "ex04" {
cd ex04-fhb
run-modflow
}

@test "ex05" {
cd ex05-mfusg1disu
run-modflow
}

@test "ex06" {
cd ex06-mfusg1disv
run-modflow
}

@test "ex07" {
cd ex07-mfusg1lgr
run-modflow
}

@test "ex08" {
cd ex08-mfusg1xt3d
run-modflow
}

@test "ex09" {
cd ex09-bump
run-modflow
}

@test "ex10" {
cd ex10-bumpnr
run-modflow
}

@test "ex11" {
cd ex11-disvmesh
run-modflow
}

@test "ex12" {
cd ex12-hanicol
run-modflow
}

@test "ex13" {
cd ex13-hanirow
run-modflow
}

@test "ex14" {
cd ex14-hanixt3d
run-modflow
}

@test "ex15" {
cd ex15-whirlsxt3d
run-modflow
}

@test "ex16" {
cd ex16-mfnwt2
run-modflow
}

@test "ex17" {
cd ex17-mfnwt3h
run-modflow
}

@test "ex18" {
cd ex18-mfnwt3l
run-modflow
}

@test "ex19" {
cd ex19-zaidel
run-modflow
}

@test "ex20" {
cd ex20-keating
run-modflow
}

@test "ex21" {
cd ex21-sfr1
run-modflow
}

@test "ex22" {
cd ex22-lak2
run-modflow
}

@test "ex23" {
cd ex23-lak4
run-modflow
}

@test "ex24" {
cd ex24-neville
run-modflow
}

@test "ex25" {
cd ex25-flowing-maw
run-modflow
}

@test "ex26" {
cd ex26-Reilly-maw
run-modflow
}

@test "ex27" {
cd ex27-advpakmvr
run-modflow
}

@test "ex28" {
cd ex28-mflgr3
run-modflow
}

@test "ex29" {
cd ex29-vilhelmsen-gc
run-modflow
}

@test "ex30" {
cd ex30-vilhelmsen-gf
run-modflow
}

@test "ex31" {
cd ex31-vilhelmsen-lgr
run-modflow
}

@test "ex32" {
cd ex32-periodicbc
run-modflow
}
