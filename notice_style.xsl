<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:fo="http://www.w3.org/1999/XSL/Format">

  <xsl:output method="xml" indent="yes"/>

  <xsl:template match="/">
    <fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">

      <fo:layout-master-set>
        <fo:simple-page-master master-name="A4"
          page-height="29.7cm" page-width="21cm" margin="2cm">
          <fo:region-body/>
        </fo:simple-page-master>
      </fo:layout-master-set>

      <fo:page-sequence master-reference="A4">
        <fo:flow flow-name="xsl-region-body">

          <!-- タイトル -->
          <fo:block text-align="center" font-size="16pt" font-weight="bold"
                    font-family="MS Mincho" space-after="20pt">
            標準報酬月額決定通知書
          </fo:block>

          <!-- 発行情報 -->
          <fo:block font-size="10pt" font-family="MS Mincho" space-after="10pt">
            宛名：<xsl:value-of select="標準報酬決定通知書/宛名"/>
          </fo:block>
          <fo:block font-size="10pt" font-family="MS Mincho" space-after="10pt">
            発行日：<xsl:value-of select="標準報酬決定通知書/発行日"/>
          </fo:block>

          <!-- 情報表 -->
          <fo:table table-layout="fixed" width="100%" border="solid 1pt black"
                    font-family="MS Mincho" margin-top="20pt">
            <fo:table-column column-width="5cm"/>
            <fo:table-column column-width="*"/>
            <fo:table-body>

              <xsl:for-each select="標準報酬決定通知書/被保険者/*">
                <fo:table-row>
                  <fo:table-cell border="solid 0.5pt black" padding="4pt">
                    <fo:block><xsl:value-of select="name()"/></fo:block>
                  </fo:table-cell>
                  <fo:table-cell border="solid 0.5pt black" padding="4pt">
                    <fo:block><xsl:value-of select="."/></fo:block>
                  </fo:table-cell>
                </fo:table-row>
              </xsl:for-each>

            </fo:table-body>
          </fo:table>

          <!-- フッター -->
          <fo:block space-before="30pt" font-size="10pt" text-align="right"
                    font-family="MS Mincho">
            日本年金機構 支部長
          </fo:block>

        </fo:flow>
      </fo:page-sequence>
    </fo:root>
  </xsl:template>
</xsl:stylesheet>
