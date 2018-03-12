<template>
  <div class="text-left">
    <h2>Assay Screening Allocation Rules Script Language</h2>
    <h2>Specification Version: ver-1</h2>
    <p>&nbsp;</p>
    <h1>Getting Started</h1>
    <p>&nbsp;</p>
    <p style="margin-left: 36.0pt;">
      <span style="font-family: 'Courier New';">P Plate1</span>
    </p>
    <p style="margin-left: 36.0pt;">
      <span style="font-family: 'Courier New';">
        A
        Titanium-Taq&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        1-12&nbsp; A-H 0.02 M/uL
      </span>
    </p>
    <p style="margin-left: 36.0pt;">
      <span style="font-family: 'Courier New';">
        A (Eco)-ATCC-BAA-2355&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1,5,9 B&nbsp;&nbsp;
        1.16 x
      </span>
    </p>
    <p>
      <span style="font-family: 'Courier New';">&nbsp;</span>
    </p>
    <ul>
      <li>
        The first letter of each line says what type of rule it is. (P,A,T,V)
      </li>
      <li>
        The first line means &ldquo;I&rsquo;m talking about a{' '}
        <strong>plate</strong> that I&rsquo;m going to call Plate1&rdquo;
      </li>
      <li>
        I want to allocate the <em>reagent</em> Titanium-Taq to the range of
        cells denoted by these columns/rows, at the concentration specified.
      </li>
      <li>
        Note the three ways you can specify which cells you mean{' '}
        <em>(single, range, list)</em>
      </li>
      <li>
        The fields are separated by one or more spaces; you don&rsquo;t have to
        line things up like I have.
      </li>
      <li>Everything is case-sensitive.</li>
      <li>
        The concentration units must be one of a fixed list known to the
        language interpreter.
      </li>
      <li>
        You are not allowed to use tabs in your script<em>
          <span style="font-size: 10.0pt; line-height: 107%;">
            . (to make it easier for an editor tool to line columns up
            automatically for you).
          </span>
        </em>
      </li>
    </ul>
    <h1>Addition Plates, and Transfers</h1>
    <p>&nbsp;</p>
    <p style="margin-left: 36.0pt;">
      <span style="font-family: 'Courier New';">P Plate1</span>
    </p>
    <p style="margin-left: 36.0pt;">
      <span style="font-family: 'Courier New';">&hellip;</span>
    </p>
    <p style="margin-left: 36.0pt;">
      <span style="font-family: 'Courier New';">&nbsp;</span>
    </p>
    <p style="margin-left: 36.0pt;">
      <span style="font-family: 'Courier New';">P Plate42</span>
    </p>
    <p style="margin-left: 36.0pt;">
      <span style="font-family: 'Courier New';">
        T Plate1 1
        B&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        1-12&nbsp; A-H&nbsp;&nbsp; 20 dilution
      </span>
    </p>
    <p>
      <span style="font-family: 'Courier New';">&nbsp;</span>
    </p>
    <ul>
      <li>Now I&rsquo;m talking about &ldquo;Plate42&rdquo;</li>
      <li>
        I want to transfer-in, stuff from cell 1B{' '}
        <em>
          <span style="font-size: 9.0pt; line-height: 107%;">
            (the source-cell
          </span>
        </em>) of &ldquo;Plate1&rdquo; into the range of cells denoted by these
        columns/rows, at the dilution specified.
      </li>
      <li>
        You can specify the <em>source-cell</em> row(s) and column(s) as either{' '}
        <em>(single, range, list). </em>But beware some combinations of
        source/destination are meaningless.
      </li>
    </ul>
    <h1>Coupons</h1>
    <p>&nbsp;</p>
    <p style="margin-left: 36.0pt;">
      <span style="font-family: 'Courier New';">P Coupon3</span>
    </p>
    <p>
      <span style="font-family: 'Courier New';">&nbsp;</span>
    </p>
    <ul>
      <li>
        The language makes no distinction between a plate, a coupon, or any
        other type of container arrangement; they are all just a P.
      </li>
      <li>
        A plate, as far as this language is concerned is just a thing that has
        rows and columns, and to which you give a name.
      </li>
      <li>Use the name to convey meaning to humans reading the script.</li>
      <li>
        It&rsquo;s up to you to avoid using cells other than A1 for coupons.
      </li>
    </ul>
    <h1>Registration of Legal Reagent Names</h1>
    <p>
      The software that interprets these rules, knows in advance which reagent
      names are allowed, and will treat a non-recognized one as an error in your
      script.
    </p>
    <p>
      If you end a reagent name with an exclamation mark &lsquo;!&rsquo;, the
      system will treat this as an instruction to add this name (without the !)
      to its set of allowed names.
    </p>
    <p style="margin-left: 36.0pt;">
      <span style="font-family: 'Courier New';">
        A
        some-new-reagent!&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        1-12&nbsp; A-H 0.02 M/uL
      </span>
    </p>
    <h1>Reagent Lot-Numbers</h1>
    <p>
      There are no such-thing as lot numbers as far as this language is
      concerned.
    </p>
    <p>
      You should incorporate it into the reagent name, however you wish. For
      example:
    </p>
    <p style="margin-left: 36.0pt;">
      <span style="font-family: 'Courier New';">
        A
        TAQ-lot99&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        1-12&nbsp; A-H 0.02 M/uL
      </span>
    </p>
    <h1>Comments and Blank Lines</h1>
    <p>
      Any line that starts with &lsquo;#&rsquo; is a comment for humans and is
      ignored by the language interpreter.
    </p>
    <p>The same goes for completely blank lines.</p>
    <h1>Specifying the Version of the Language You are Using</h1>
    <p>The first line of your script must be of this form:</p>
    <p style="margin-left: 36.0pt;">
      <span style="font-family: 'Courier New';">V ver-1</span>
    </p>
    <p>
      This proclaims which language specification version you are conforming to
      with the rules in your script.
    </p>
    <p>
      This allows us to extend the syntax and capabilities in the future whilst
      still being able to interpret scripts that conform to older versions.
      (Note the title of this document says that it is ver-3).
    </p>
  </div>
</template>;
